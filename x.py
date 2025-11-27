from flask import Flask, request, make_response, render_template
import mysql.connector
import re 
import dictionary

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

import json

import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)

UPLOAD_ITEM_FOLDER = './images'


##############################
# Multilanguage / Google Sheets setup
allowed_languages = ["english", "danish", "spanish"]
default_language = "english"
google_spread_sheet_key = "YOUR_SPREADSHEET_KEY"  # placeholder

# For exam / local testing: do not expose real service account
# If you want to test without Google Sheets, just load a local dictionary
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    # Authenticate with Google Sheets using the service account
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)

    # Open the sheet and fetch all rows
    sheet = client.open_by_key(google_spread_sheet_key).sheet1
    rows = sheet.get_all_records()
    
    # Build the dictionary for translations
    dictionary = {}
    for row in rows:
        key = row['key']
        dictionary[key] = {lang: row[lang] for lang in allowed_languages}

except Exception as e:
    # Fallback to local dictionary.json for testing without real credentials
    import json
    with open("dictionary.json", "r", encoding="utf-8") as f:
        dictionary = json.load(f)

# Function to get translation
def lans(key, lang=None):
    lang = lang if lang in allowed_languages else default_language
    return dictionary.get(key, {}).get(lang, key)



#####################################
def db():
    try:
        db = mysql.connector.connect(
            host="x_mariadb0",
            user="root",
            password="password",
            database="x",
            ssl_disabled=True  
        )
        cursor = db.cursor(dictionary=True)
        return db, cursor
    except mysql.connector.Error as e:
        print("MySQL Error:", e, flush=True)
        raise Exception("Database under maintenance", 500)


##############################
def no_cache(view):
    @wraps(view)
    def no_cache_view(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    return no_cache_view


##############################
REGEX_EMAIL = r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"
def validate_user_email(lan = "en"):
    user_email = request.form.get("user_email", "").strip()
    if not re.match(REGEX_EMAIL, user_email): raise Exception(dictionary.invalid_email[lan], 400)
    return user_email

##############################
USER_USERNAME_MIN = 2
USER_USERNAME_MAX = 20
REGEX_USER_USERNAME = f"^.{{{USER_USERNAME_MIN},{USER_USERNAME_MAX}}}$"
def validate_user_username():
    user_username = request.form.get("user_username", "").strip()
    error = f"username min {USER_USERNAME_MIN} max {USER_USERNAME_MAX} characters"
    if len(user_username) < USER_USERNAME_MIN: raise Exception(error, 400)
    if len(user_username) > USER_USERNAME_MAX: raise Exception(error, 400)
    return user_username

##############################
USER_FIRST_NAME_MIN = 2
USER_FIRST_NAME_MAX = 20
REGEX_USER_FIRST_NAME = f"^.{{{USER_FIRST_NAME_MIN},{USER_FIRST_NAME_MAX}}}$"
def validate_user_first_name():
    user_first_name = request.form.get("user_first_name", "").strip()
    error = f"first name min {USER_FIRST_NAME_MIN} max {USER_FIRST_NAME_MAX} characters"
    if not re.match(REGEX_USER_FIRST_NAME, user_first_name): raise Exception(error, 400)
    return user_first_name

##############################
USER_LAST_NAME_MIN = 2
USER_LAST_NAME_MAX = 20
REGEX_USER_LAST_NAME = f"^.{{{USER_LAST_NAME_MIN},{USER_LAST_NAME_MAX}}}$"
def validate_user_last_name():
    user_last_name = request.form.get("user_last_name", "").strip()
    error = f"last name min {USER_LAST_NAME_MIN} max {USER_LAST_NAME_MAX} characters"
    if not re.match(REGEX_USER_LAST_NAME, user_last_name): raise Exception(error, 400)
    return user_last_name

##############################
USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
REGEX_USER_PASSWORD = f"^.{{{USER_PASSWORD_MIN},{USER_PASSWORD_MAX}}}$"
def validate_user_password(lan = "en"):
    user_password = request.form.get("user_password", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password): raise Exception(dictionary.invalid_password[lan], 400)
    return user_password




##############################
def validate_user_password_confirm():
    user_password = request.form.get("user_password_confirm", "").strip()
    if not re.match(REGEX_USER_PASSWORD, user_password): raise Exception("Twitter exception - Invalid confirm password", 400)
    return user_password


##############################
REGEX_UUID4 = "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
def validate_uuid4(uuid4 = ""):
    if not uuid4:
        uuid4 = request.values.get("uuid4", "").strip()
    if not re.match(REGEX_UUID4, uuid4): raise Exception("Twitter exception - Invalid uuid4", 400)
    return uuid4


##############################
REGEX_UUID4_WITHOUT_DASHES = "^[0-9a-f]{8}[0-9a-f]{4}4[0-9a-f]{3}[89ab][0-9a-f]{3}[0-9a-f]{12}$"
def validate_uuid4_without_dashes(uuid4 = ""):
    error = "Invalid uuid4 without dashes"
    if not uuid4: raise Exception(error, 400)
    uuid4 = uuid4.strip()
    if not re.match(REGEX_UUID4_WITHOUT_DASHES, uuid4): raise Exception(error, 400)
    return uuid4

##############################
POST_MIN_LEN = 2
POST_MAX_LEN = 250
REGEX_POST = f"^.{{{POST_MIN_LEN},{POST_MAX_LEN}}}$"
def validate_post(post = ""):
    post = post.strip()
    if not re.match(REGEX_POST, post): raise Exception("x-error post", 400)
    return post

##############################
COMMENT_MIN_LEN = 1
COMMENT_MAX_LEN = 250
REGEX_COMMENT = f"^.{{{COMMENT_MIN_LEN},{COMMENT_MAX_LEN}}}$"

def validate_comment(comment=""):
    comment = comment.strip()
    if not re.match(REGEX_COMMENT, comment):
        raise Exception("x-error comment", 400)
    return comment


##############################
def send_email(to_email, subject, template):
    try:
        # Create a gmail fullflaskdemomail
        # Enable (turn on) 2 step verification/factor in the google account manager
        # Visit: https://myaccount.google.com/apppasswords
        # Copy the key : pdru ctfd jdhk xxci

        # Email and password of the sender's Gmail account
        sender_email = "sophieteinvigkjer@gmail.com"
        password = "tsmm iisu acbv zppl"  # If 2FA is on, use an App Password instead

        # Receiver email address
        receiver_email = to_email
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "X clone"
        message["To"] = to_email
        message["Subject"] = subject

        # Body of the email
        message.attach(MIMEText(template, "html"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        ic("Email sent successfully!")

        return "email sent"
       
    except Exception as ex:
        ic(ex)
        raise Exception("cannot send email", 500)
    finally:
        pass