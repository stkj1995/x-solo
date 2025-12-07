from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from markupsafe import escape
from itsdangerous import URLSafeTimedSerializer
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import requests

import os
import re
import io
import csv
import json
import time
import uuid
import random
import hashlib
import x
import dictionary
import base64
import datetime
import traceback
from icecream import ic
from functools import wraps
# from dotenv import load_dotenv

import sys
import os

# Add your project path
project_home = '/home/teinvig/x-solo'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Activate virtualenv
activate_this = '/home/teinvig/x-solo/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Flask app from your new main file
from app import app as application

ic.configureOutput(prefix='----- | ', includeContext=True)

app = Flask(__name__, static_folder="static")

app.config["DEBUG"] = True
app.secret_key = "SECRET_KEY"

# Set maximum file upload size (10 MB)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# Session Configuration
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Serializer for token generation
s = URLSafeTimedSerializer(app.secret_key)
user_verification_key = uuid.uuid4().hex
verify_token = str(uuid.uuid4())

def verify_scrypt_password(stored, provided):
    """
    Verify a password stored with scrypt.
    Stored format: scrypt:N:r:p$salt$hash
    """
    parts = stored.split('$')
    if len(parts) != 3:
        return False

    params, salt_b64, hash_b64 = parts
    N, r, p = map(int, params.split(':')[1:])
    salt = base64.b64decode(salt_b64)
    stored_hash = base64.b64decode(hash_b64)

    test_hash = hashlib.scrypt(
        provided.encode(),
        salt=salt,
        n=N,
        r=r,
        p=p,
        maxmem=0,
        dklen=len(stored_hash)
    )
    return test_hash == stored_hash

# Folder for user-uploaded media
UPLOAD_FOLDER = 'static/uploads'          # <-- your folder path
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'heic'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Make sure the folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

##############################
##############################
##############################
def _____USER_____(): pass 
##############################
##############################
##############################

@app.get("/")
def view_index():
   
    return render_template("index.html")

##############################
@app.context_processor
def global_variables():
    return dict (
        dictionary = dictionary,
        x = x
    )
# ---------------------------
# Admin required decorator
# ---------------------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

# ---------------------------
# Admin login
# ---------------------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db, cursor = x.db()  # your database connection
        try:
            cursor.execute("SELECT * FROM admin WHERE admin_email=%s", (email,))
            admin = cursor.fetchone()

            if not admin:
                error = "Email not found"
            elif not check_password_hash(admin["admin_password"], password):
                error = "Incorrect password"
            else:
                # login successful
                session["admin"] = admin
                return redirect(url_for("admin"))  # replace with your admin page

        finally:
            cursor.close()
            db.close()

    return render_template("_admin_login.html", error=error)

# ---------------------------
# Admin dashboard
# ---------------------------
@app.route("/admin", defaults={'lan': None})
@app.route("/admin/<lan>")
@admin_required
def admin(lan=None):
    try:
        # --- Language handling ---
        if lan not in x.allowed_languages:
            lan = x.default_language  # fallback
        session["admin_lang"] = lan  # store admin's selected language
        x.default_language = lan     # ensure x.lans() uses it

        admin_session = session.get("admin")

        # Pagination
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 20))
        offset = (page - 1) * per_page

        db, cursor = x.db()

        # USERS TABLE + LANGUAGE
        cursor.execute("""
            SELECT 
                user_pk, 
                user_email, 
                user_blocked, 
                user_first_name, 
                user_last_name, 
                user_role,
                user_language_fk
            FROM users
            ORDER BY user_pk
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        users = cursor.fetchall()

        # Total count
        cursor.execute("SELECT COUNT(*) AS total FROM users")
        total_users = cursor.fetchone()["total"]
        total_pages = (total_users + per_page - 1) // per_page

        # POSTS TABLE
        cursor.execute("""
            SELECT 
                posts.post_pk, 
                posts.post_user_fk, 
                posts.post_message, 
                posts.post_blocked, 
                users.user_email
            FROM posts
            LEFT JOIN users ON posts.post_user_fk = users.user_pk
            ORDER BY posts.post_pk
        """)
        posts = cursor.fetchall()

        cursor.close()
        db.close()

        return render_template(
            "admin.html",
            admin=admin_session,
            users=users,
            posts=posts,
            page=page,
            per_page=per_page,
            total_pages=total_pages,
            languages=x.allowed_languages,  # for flag selection
            lan=lan
        )

    except Exception as ex:
        traceback.print_exc()
        return f"System error: {ex}", 500

# ---------------------------
# Block/unblock user
# ---------------------------
@app.route("/admin/block_user/<user_pk>", methods=["POST"])
@admin_required
def block_user(user_pk):
    db, cursor = x.db()  # your function to get db connection
    cursor.execute("SELECT user_blocked, user_email FROM users WHERE user_pk=%s", (user_pk,))
    user = cursor.fetchone()

    if not user:
        cursor.close()
        db.close()
        return "User not found", 404

    # Toggle blocked status
    new_status = 0 if user["user_blocked"] else 1
    cursor.execute("UPDATE users SET user_blocked=%s WHERE user_pk=%s", (new_status, user_pk))
    db.commit()
    cursor.close()
    db.close()

    status_text = "unblocked" if new_status == 0 else "blocked"
    x.send_email(user["user_email"], "Account status updated", f"Your account has been {status_text} by the administrator.")

    return redirect(url_for("admin"))

# ---------------------------
# Block/unblock post
# ---------------------------
@app.route("/admin/block_post/<post_pk>", methods=["POST"])
@admin_required
def block_post(post_pk):
    db, cursor = x.db()
    cursor.execute("""
        SELECT post_blocked, users.user_email
        FROM posts
        JOIN users ON posts.post_user_fk = users.user_pk
        WHERE post_pk=%s
    """, (post_pk,))
    post = cursor.fetchone()

    if not post:
        cursor.close()
        db.close()
        return "Post not found", 404

    new_status = 0 if post["post_blocked"] else 1
    cursor.execute("UPDATE posts SET post_blocked=%s WHERE post_pk=%s", (new_status, post_pk))
    db.commit()
    cursor.close()
    db.close()

    status_text = "unblocked" if new_status == 0 else "blocked"
    x.send_email(post["user_email"], "Post status updated", f"Your post has been {status_text} by the administrator.")

    return redirect(url_for("admin"))

# ---------------------------
# Admin logout
# ---------------------------
@app.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

################################
@app.route("/login", defaults={'lan': 'english'}, methods=["GET", "POST"])
@app.route("/login/<lan>", methods=["GET", "POST"])
@x.no_cache
def login(lan="english"):
    # --- Language handling ---
    if lan not in x.allowed_languages:
        lan = "english"
    x.default_language = lan

    # --- GET = show login page ---
    if request.method == "GET":
        if session.get("user"):
            return redirect(url_for("home"))
        return render_template("login.html", lan=lan)

    # --- POST = process login ---
    if request.method == "POST":
        try:
            # Read data from JSON or form
            data = request.get_json(force=True) if request.is_json else request.form
            user_email = (data.get("user_email") or "").strip()
            user_password = (data.get("user_password") or "").strip()

            # --- Required fields ---
            if not user_email or not user_password:
                raise Exception(dictionary.invalid_credentials[lan], 400)

            # --- Email format ---
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, user_email):
                raise Exception(dictionary.invalid_credentials[lan], 400)

            # Optional: sanitize email input
            user_email = escape(user_email)

            # --- Fetch user from DB ---
            db_conn, cursor = x.db()
            cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
            user = cursor.fetchone()

            if not user:
                raise Exception(dictionary.user_not_found[lan], 400)

            # --- Check password ---
            print("Checking password...")
            if not check_password_hash(user["user_password"], user_password):
                print("Password incorrect")
                # Optional: track failed login attempts here for rate-limiting
                raise Exception(dictionary.invalid_credentials[lan], 400)

            # --- Check email verification ---
            print("Checking verification....")
            if user.get("user_verification_key", "") != "":
                print("User not verified")
                raise Exception(dictionary.user_not_verified[lan], 400)

            # --- Remove password and set session ---
            user.pop("user_password", None)
            session["user"] = user

            # --- Success redirect ---
            return f"""<mixhtml mix-redirect="{url_for('home')}"></mixhtml>"""

        except Exception as ex:
            ic(ex)
            # --- Validation / user errors ---
            if len(ex.args) > 1 and ex.args[1] == 400:
                toast_error = render_template("___toast_error.html", message=ex.args[0])
                return f"""<mixhtml mix-update="#toast">{toast_error}</mixhtml>""", 400

            # --- System error ---
            toast_error = render_template("___toast_error.html", message="System under maintenance")
            return f"""<mixhtml mix-bottom="#toast">{toast_error}</mixhtml>""", 500

        finally:
            if "cursor" in locals(): cursor.close()
            if "db_conn" in locals(): db_conn.close()

#############################
def send_verify_email(user_email, user_verification_key):
    verification_link = f"http://127.0.0.1/verify-account?key={user_verification_key}"
    subject = "Verify your account"
    body = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <p>Hi! Click below to verify your account:</p>
        <a href="{verification_link}">Verify Account</a>
      </body>
    </html>
    """
    x.send_email(user_email, subject, body)

###########################
@app.route("/signup", defaults={'lan': 'english'}, methods=["GET", "POST"])
@app.route("/signup/<lan>", methods=["GET", "POST"])
def signup(lan):
    # --- Language handling ---
    if lan not in x.allowed_languages:
        lan = "english"
    x.default_language = lan

    # --- GET = show signup page ---
    if request.method == "GET":
        return render_template("signup.html", lan=lan)

    # --- POST = process signup ---
    try:
        # Read data from JSON or form
        data = request.get_json(force=True) if request.is_json else request.form
        user_email = (data.get("user_email") or "").strip()
        user_password = (data.get("user_password") or "").strip()
        user_username = (data.get("user_username") or "").strip()
        user_first_name = (data.get("user_first_name") or "").strip()

        # --- Required fields ---
        if not user_email or not user_password or not user_username or not user_first_name:
            raise Exception("All fields are required", 400)

        # --- Email format ---
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, user_email):
            raise Exception("Invalid email format", 400)

        # --- Password rules ---
        if len(user_password) < 8:
            raise Exception("Password must be at least 8 characters", 400)
        if not re.search(r'\d', user_password):
            raise Exception("Password must contain at least one number", 400)
        if not re.search(r'[A-Z]', user_password):
            raise Exception("Password must contain at least one uppercase letter", 400)
        if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', user_password):
            raise Exception("Password must contain at least one symbol", 400)

        # --- Username rules ---
        if len(user_username) < 3 or len(user_username) > 20:
            raise Exception("Username must be 3-20 characters", 400)
        if not re.match(r'^\w+$', user_username):
            raise Exception("Username can only contain letters, numbers, and underscores", 400)

        # --- Sanitize inputs ---
        user_first_name = escape(user_first_name)
        user_username = escape(user_username)

        # --- Hash password ---
        user_hashed_password = generate_password_hash(user_password)

        # --- Generate user data ---
        user_pk = uuid.uuid4().hex
        user_last_name = ""
        user_avatar_path = "https://avatar.iran.liara.run/public/40"
        user_verification_key = uuid.uuid4().hex
        user_verified_at = 0

        # --- Insert into database ---
        q = """INSERT INTO users 
        (user_pk, user_email, user_password, user_username, user_first_name,
         user_last_name, user_avatar_path, user_verification_key, user_verified_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        db, cursor = x.db()
        cursor.execute(q, (
            user_pk, user_email, user_hashed_password,
            user_username, user_first_name, user_last_name,
            user_avatar_path, user_verification_key, user_verified_at
        ))
        db.commit()

        # --- Send verification email ---
        send_verify_email(user_email, user_verification_key)

        # --- Success → redirect to login ---
        return f"""<mixhtml mix-redirect="{url_for('login')}"></mixhtml>""", 200

    except Exception as ex:
        ic(ex)

        # --- USER ERRORS (validation) ---
        if len(ex.args) > 1 and ex.args[1] == 400:
            toast = render_template("___toast_error.html", message=ex.args[0])
            return f"""<mixhtml mix-update="#toast">{toast}</mixhtml>""", 400

        # --- DATABASE ERRORS (duplicate email or username) ---
        error_message = str(ex)
        if "Duplicate entry" in error_message:
            if user_email in error_message:
                msg = "Email already registered"
            elif user_username in error_message:
                msg = "Username already registered"
            else:
                msg = "Account already exists"
            toast = render_template("___toast_error.html", message=msg)
            return f"""<mixhtml mix-update='#toast'>{toast}</mixhtml>""", 400

        # --- SYSTEM ERROR ---
        toast = render_template("___toast_error.html", message="System error. Try again later.")
        return f"""<mixhtml mix-bottom='#toast'>{toast}</mixhtml>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# VERIFY ACCOUNT #############################
@app.route("/verify-account", methods=["GET"])
def verify_account():
    try:
        user_verification_key = x.validate_uuid4_without_dashes(request.args.get("key", ""))
        user_verified_at = int(time.time())
        db, cursor = x.db()
        q = "UPDATE users SET user_verification_key = '', user_verified_at = %s WHERE user_verification_key = %s"
        cursor.execute(q, (user_verified_at, user_verification_key))
        db.commit()
        if cursor.rowcount != 1: raise Exception("Invalid key", 400)
        return redirect( url_for('login') )
    except Exception as ex:
        ic(ex)
        if "db" in locals(): db.rollback()
        # User errors
        if ex.args[1] == 400: return ex.args[0], 400    

        # System or developer error
        return "Cannot verify user"

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##############################
@app.get("/logout")
def logout():
    try:
        session.clear()
        return redirect(url_for("login"))
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

# HOME PAGE
@app.route("/home")
def home():
    user = session.get("user")  # logged-in user
    if not user:
        return redirect(url_for("login"))

    db, cursor = x.db()
    try:
        # ----------------- Fetch posts -----------------
        cursor.execute("""
            SELECT p.post_pk, p.post_user_fk, p.post_message, p.post_image_path, 
                   p.post_total_likes, p.created_at,
                   u.user_first_name, u.user_last_name, u.user_username, u.user_avatar_path
            FROM posts p
            JOIN users u ON p.post_user_fk = u.user_pk
            ORDER BY p.created_at DESC
        """)
        tweets = cursor.fetchall()

        # Fetch comments for each tweet
        for t in tweets:
            cursor.execute("""
                SELECT c.comment_pk, c.comment_post_fk, c.comment_user_fk,
                       c.comment_message, c.created_at,
                       u.user_first_name, u.user_last_name
                FROM comments c
                JOIN users u ON u.user_pk = c.comment_user_fk
                WHERE c.comment_post_fk = %s
                ORDER BY c.created_at ASC
            """, (t["post_pk"],))
            t["comments"] = cursor.fetchall() or []
            t["comment_count"] = len(t["comments"])
            t["liked_by_user"] = False  # Needed for _tweet.html

        # ----------------- Who to follow suggestions -----------------
        cursor.execute("""
            SELECT u.user_pk, u.user_first_name, u.user_last_name, u.user_username, u.user_avatar_path
            FROM users u
            WHERE u.user_pk != %s
            ORDER BY RAND()
            LIMIT 5
        """, (user["user_pk"],))
        suggestions = cursor.fetchall()

        # ----------------- Get current user's follows -----------------
        cursor.execute("""
            SELECT follow_target_fk
            FROM follows
            WHERE follow_user_fk = %s
        """, (user["user_pk"],))
        follows = cursor.fetchall()  # list of dicts with 'follow_target_fk'

        # ----------------- Fetch active trends -----------------
        cursor.execute("""
            SELECT trend_pk, trend_title, trend_message, trend_user_fk, trend_image, created_at
            FROM trends
            WHERE is_active = 1
            ORDER BY created_at DESC
            LIMIT 4
        """)
        trends = cursor.fetchall()

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

    return render_template(
        "home.html",
        tweets=tweets,
        user=user,
        suggestions=suggestions,
        follows=follows,
        trends=trends  # <-- pass trends to template
    )

# COMPONENT FOR AJAX UPDATES (feed only)
@app.get("/home-comp")
def home_comp():
    user = session.get("user")
    if not user:
        return "error"

    db, cursor = x.db()
    try:
        # ----------------- Fetch latest posts -----------------
        cursor.execute("""
            SELECT p.post_pk, p.post_user_fk, p.post_message, p.post_image_path,
                   p.created_at AS post_created_at,
                   u.user_first_name, u.user_last_name, u.user_username, u.user_avatar_path
            FROM posts p
            JOIN users u ON u.user_pk = p.post_user_fk
            ORDER BY p.created_at DESC
            LIMIT 20
        """)
        tweets = cursor.fetchall()

        # Fetch comments for each tweet
        for t in tweets:
            cursor.execute("""
                SELECT c.comment_pk, c.comment_post_fk, c.comment_user_fk,
                       c.comment_message, c.created_at,
                       u.user_first_name, u.user_last_name
                FROM comments c
                JOIN users u ON u.user_pk = c.comment_user_fk
                WHERE c.comment_post_fk = %s
                ORDER BY c.created_at ASC
            """, (t["post_pk"],))
            t["comments"] = cursor.fetchall() or []
            t["comment_count"] = len(t["comments"])
            t["liked_by_user"] = False

        # Render only the feed component
        html = render_template("_home_comp.html", tweets=tweets, user=user)
        return f"""<mixhtml mix-update="feed">{html}</mixhtml>"""  # <-- updates only #feed

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# PROFILE #############################
@app.get("/profile")
def profile():
    try:
        user = session.get("user", "")
        if not user: return "error"
        q = "SELECT * FROM users WHERE user_pk = %s"
        db, cursor = x.db()
        cursor.execute(q, (user["user_pk"],))
        user = cursor.fetchone()
        profile_html = render_template("_profile.html", x=x, user=user)
        return f"""<browser mix-update="main">{ profile_html }</browser>"""
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

# API UPDATE PROFILE #############################
@app.route("/api-update-profile", methods=["POST"])
def api_update_profile():
    try:
        # --- Get logged-in user ---
        user = session.get("user")
        if not user:
            return "invalid user", 403

        db, cursor = x.db()

        # --- Validate inputs ---
        user_email = x.validate_user_email()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()
        user_last_name = x.validate_user_last_name()

        # --- Check email uniqueness (ignore soft-deleted users) ---
        cursor.execute(
            "SELECT * FROM users WHERE user_email=%s AND user_pk!=%s AND is_deleted=0",
            (user_email, user["user_pk"])
        )
        if cursor.fetchone():
            raise Exception("Email already registered")

        # --- Check username uniqueness ---
        cursor.execute(
            "SELECT * FROM users WHERE user_username=%s AND user_pk!=%s AND is_deleted=0",
            (user_username, user["user_pk"])
        )
        if cursor.fetchone():
            raise Exception("Username already taken")

        # --- Handle avatar upload ---
        avatar_file = request.files.get("useravatar")
        if avatar_file and avatar_file.filename != "":
            filename = f"{user['user_pk']}_{avatar_file.filename}"
            avatar_path = os.path.join("uploads", filename)  # store relative path
            full_path = os.path.join("static", avatar_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            avatar_file.save(full_path)
        else:
            avatar_path = user.get("user_avatar_path", "")  # keep old avatar

        # --- Update database ---
        q = """UPDATE users 
               SET user_email=%s, user_username=%s, user_first_name=%s,
                   user_last_name=%s, user_avatar_path=%s
               WHERE user_pk=%s"""
        cursor.execute(q, (user_email, user_username, user_first_name, user_last_name, avatar_path, user["user_pk"]))
        db.commit()

        # --- Update session ---
        session["user"].update({
            "user_email": user_email,
            "user_username": user_username,
            "user_first_name": user_first_name,
            "user_last_name": user_last_name,
            "user_avatar_path": avatar_path
        })

        # --- Response to frontend ---
        toast_ok = render_template("___toast_ok.html", message="Profile updated successfully")
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-update="#profile_tag .name">{user_first_name}</browser>
            <browser mix-update="#profile_tag .handle">{user_username}</browser>
        """, 200

    except Exception as ex:
        ic(ex)
        toast_error = render_template("___toast_error.html", message=str(ex))
        return f"""<mixhtml mix-update="#toast">{toast_error}</mixhtml>""", 400

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

###################################
@app.route("/toggle-like-tweet", methods=["POST", "PATCH"])
def toggle_like_tweet():
    try:
        user_pk = session.get("user")
        post_pk = request.form.get("post_pk")

        if not user_pk or not post_pk:
            return f"<mixhtml><mix-message>Missing user or post</mix-message></mixhtml>", 400

        db, cursor = x.db()

        # Check if already liked
        cursor.execute("SELECT * FROM likes WHERE like_user_fk=%s AND like_post_fk=%s", (user_pk, post_pk))
        liked = cursor.fetchone() is not None

        if liked:
            # Unlike
            cursor.execute("DELETE FROM likes WHERE like_user_fk=%s AND like_post_fk=%s", (user_pk, post_pk))
            liked = False
        else:
            # Like
            cursor.execute("INSERT INTO likes (like_pk, like_user_fk, like_post_fk, created_at) VALUES (UUID(), %s, %s, NOW())", (user_pk, post_pk))
            liked = True

        db.commit()

        # Count total likes
        cursor.execute("SELECT COUNT(*) AS total FROM likes WHERE like_post_fk=%s", (post_pk,))
        total = cursor.fetchone()["total"]

        # Render button template
        button_html = render_template("_button_like_toggle.html", tweet={"post_pk": post_pk, "post_total_likes": total, "liked_by_user": liked})

        return f"""
        <mixhtml>
            <mix-target query="[data-like-button='{post_pk}']">
                {button_html}
            </mix-target>
        </mixhtml>
        """

    except Exception as e:
        print("LIKE ERROR:", e)
        return f"<mixhtml><mix-message>{e}</mix-message></mixhtml>", 500

    finally:
        cursor.close()
        db.close()

##############################
@app.route("/api-create-post", methods=["POST"])
def api_create_post():
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    user_pk = user["user_pk"]

    # ---------------- Text ----------------
    post_text = request.form.get("post", "").strip()
    if post_text:
        try:
            post_text = x.validate_post(post_text)
        except Exception:
            pass

        if not (1 <= len(post_text) <= 5000):
            return jsonify({"success": False, "error": "Post must be 1–5000 characters"}), 400

    # ---------------- Image ----------------
    post_image_path = ""
    file = request.files.get("post_image")
    if file and file.filename:
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "Invalid file type"}), 400

        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        post_image_path = filename

    # ---------------- Validate content ----------------
    if not post_text and not post_image_path:
        return jsonify({"success": False, "error": "Cannot post empty content"}), 400

    # ---------------- Insert into DB ----------------
    post_pk = uuid.uuid4().hex

    try:
        db, cursor = x.db()
        cursor.execute("""
            INSERT INTO posts (post_pk, post_user_fk, post_message,
                               post_image_path, post_total_likes, created_at)
            VALUES (%s, %s, %s, %s, 0, NOW())
        """, (post_pk, user_pk, post_text, post_image_path))
        db.commit()

        tweet = {
            **user,
            "post_pk": post_pk,
            "post_message": post_text,
            "post_image_path": post_image_path
        }

        html_post = render_template("_tweet.html", tweet=tweet, user=user)
        return html_post

    except Exception as ex:
        if "db" in locals():
            db.rollback()
        return jsonify({"success": False, "error": str(ex)}), 500

    finally:
        if "cursor" in locals():
            cursor.close()
        if "db" in locals():
            db.close()

#################################
@app.route("/api-update-post/<post_pk>", methods=["POST"])
def api_update_post(post_pk):
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    text = request.form.get("post_message", "").strip()
    if not text:
        return jsonify({"success": False, "error": "Empty content"}), 400

    try:
        db, cursor = x.db()

        cursor.execute("SELECT post_user_fk FROM posts WHERE post_pk=%s", (post_pk,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "error": "Post not found"}), 404
        if row["post_user_fk"] != user["user_pk"]:
            return jsonify({"success": False, "error": "Not allowed"}), 403

        cursor.execute(
            "UPDATE posts SET post_message=%s WHERE post_pk=%s",
            (text, post_pk)
        )
        db.commit()

        return jsonify({"success": True, "post_message": text})

    except Exception as ex:
        if "db" in locals(): db.rollback()
        return jsonify({"success": False, "error": str(ex)}), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

##################################
@app.route("/api-delete-post/<post_pk>", methods=["POST"])
def api_delete_post(post_pk):
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    try:
        db, cursor = x.db()

        cursor.execute("SELECT post_user_fk FROM posts WHERE post_pk=%s", (post_pk,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "error": "Post not found"}), 404

        if row["post_user_fk"] != user["user_pk"]:
            return jsonify({"success": False, "error": "Not allowed"}), 403

        cursor.execute("DELETE FROM posts WHERE post_pk=%s", (post_pk,))
        db.commit()

        return jsonify({"success": True})

    except Exception as ex:
        if "db" in locals(): db.rollback()
        return jsonify({"success": False, "error": str(ex)}), 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# API SEARCH #############################
@app.route("/api-search-json", methods=["POST"])
def api_search_json():
    try:
        data = request.get_json()
        search_for = data.get("search_for", "").strip()

        if not search_for:
            return jsonify({"users": [], "posts": [], "trends": []})

        db, cursor = x.db()  # your db connection

        # ---------------- USERS ----------------
        cursor.execute("""
            SELECT user_pk, user_first_name, user_last_name, user_username, user_avatar_path
            FROM users
            WHERE user_first_name LIKE %s
               OR user_last_name LIKE %s
               OR user_username LIKE %s
            LIMIT 10
        """, (f"%{search_for}%", f"%{search_for}%", f"%{search_for}%"))
        users = cursor.fetchall()

        # ---------------- POSTS ----------------
        cursor.execute("""
            SELECT post_pk, post_message
            FROM posts
            WHERE post_message LIKE %s
            LIMIT 10
        """, (f"%{search_for}%", ))
        posts = cursor.fetchall()

        # ---------------- TRENDS ----------------
        cursor.execute("""
            SELECT trend_pk, trend_title, trend_message
            FROM trends
            WHERE trend_title LIKE %s
               OR trend_message LIKE %s
            LIMIT 5
        """, (f"%{search_for}%", f"%{search_for}%"))
        trends = cursor.fetchall()

        return jsonify({
            "users": users,
            "posts": posts,
            "trends": trends
        })

    except Exception as ex:
        print("SEARCH ERROR:", ex)
        return jsonify({"error": str(ex)}), 500

##############################
@app.get("/get-data-from-sheet")
def get_data_from_sheet():
    try:

        # Check if the admin is running this end-point, else show error

        # flaskwebmail
        # Create a google sheet
        # share and make it visible to "anyone with the link"
        # In the link, find the ID of the sheet. Here: 1aPqzumjNp0BwvKuYPBZwel88UO-OC_c9AEMFVsCw1qU
        # Replace the ID in the 2 places bellow
        url= f"https://docs.google.com/spreadsheets/d/{x.google_spread_sheet_key}/export?format=csv&id={x.google_spread_sheet_key}"
        res=requests.get(url=url)
        # ic(res.text) # contains the csv text structure
        csv_text = res.content.decode('utf-8')
        csv_file = io.StringIO(csv_text) # Use StringIO to treat the string as a file
        
        # Initialize an empty list to store the data
        data = {}

        # Read the CSV data
        reader = csv.DictReader(csv_file)
        ic(reader)
        # Convert each row into the desired structure
        for row in reader:
            item = {
                    'english': row['english'],
                    'danish': row['danish'],
                    'spanish': row['spanish']
                
            }
            # Append the dictionary to the list
            data[row['key']] = (item)

        # Convert the data to JSON
        json_data = json.dumps(data, ensure_ascii=False, indent=4) 
        # ic(data)

        # Save data to the file
        with open("dictionary.json", 'w', encoding='utf-8') as f:
            f.write(json_data)

        return "ok"
    except Exception as ex:
        ic(ex)
        return str(ex)
    finally:
        pass

# Example route
@app.route("/", endpoint="home_page")
def home():  # Function can keep the same name
    return "Hello Flask!"

if __name__ == "__main__":
    app.run(debug=True)

# api-follow
@app.route("/api-follow", methods=["POST"])
def api_follow():
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    following_pk = request.form.get("following_pk")
    if not following_pk:
        return jsonify({"success": False, "error": "Missing following_pk"}), 400

    try:
        db, cursor = x.db()

        # Prevent duplicate follows
        cursor.execute(
            "SELECT 1 FROM follows WHERE follow_user_fk=%s AND follow_target_fk=%s LIMIT 1",
            (user["user_pk"], following_pk)
        )
        if cursor.fetchone():
            return jsonify({"success": True})

        follow_pk = uuid.uuid4().hex
        cursor.execute(
            "INSERT INTO follows (follow_pk, follow_user_fk, follow_target_fk) VALUES (%s, %s, %s)",
            (follow_pk, user["user_pk"], following_pk)
        )
        db.commit()

        return jsonify({"success": True})

    except Exception as e:
        if "db" in locals(): db.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# api-unfollow
@app.route("/api-unfollow", methods=["POST"])
def api_unfollow():
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    following_pk = request.form.get("following_pk")
    if not following_pk:
        return jsonify({"success": False, "error": "Missing following_pk"}), 400

    try:
        db, cursor = x.db()

        cursor.execute(
            "DELETE FROM follows WHERE follow_user_fk=%s AND follow_target_fk=%s",
            (user["user_pk"], following_pk)
        )
        db.commit()

        return jsonify({"success": True})

    except Exception as e:
        if "db" in locals(): db.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# SOFT DELETE
@app.post("/delete-user")
def delete_user():
    user_pk = request.form.get("user_pk")
    if not user_pk:
        return "Invalid user ID", 400

    db, cursor = x.db()
    try:
        # Soft delete
        cursor.execute("UPDATE users SET is_deleted = 1 WHERE user_pk = %s", (user_pk,))
        db.commit()
        # Log out
        session.pop("user", None)
        # Return small HTML fragment
        return render_template("partials/deleted_message.html")
    finally:
        cursor.close()
        db.close()

# RESTORE USER
@app.post("/restore-user")
def restore_user():
    user_pk = request.form.get("user_pk")
    if not user_pk:
        return "Invalid user ID", 400

    db, cursor = x.db()
    try:
        cursor.execute("UPDATE users SET is_deleted = 0 WHERE user_pk = %s", (user_pk,))
        db.commit()
        return redirect(url_for("profile"))
    except Exception as ex:
        db.rollback()
        print("Error restoring user:", ex)
        return "An error occurred while restoring the user", 500
    finally:
        cursor.close()
        db.close()

######################################
@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "GET":
        return render_template("forgot_password.html")

    if request.method == "POST":
        try:
            user_email = (request.form.get("user_email") or "").strip()
            if not user_email:
                raise Exception("Email is required", 400)

            # Validate email format
            if not re.match(x.REGEX_EMAIL, user_email):
                raise Exception("Invalid email format", 400)

            # Fetch user
            db_conn, cursor = x.db()
            cursor.execute("SELECT * FROM users WHERE user_email = %s", (user_email,))
            user = cursor.fetchone()
            if not user:
                raise Exception("User not found", 400)

            # Generate token + expiry
            import uuid, datetime
            reset_token = str(uuid.uuid4())
            expiry = datetime.datetime.now() + datetime.timedelta(hours=1)

            cursor.execute(
                "UPDATE users SET reset_token=%s, reset_expiry=%s WHERE user_email=%s",
                (reset_token, expiry, user_email)
            )
            db_conn.commit()

            # Send email
            from send_mail import send_reset_password_email
            send_reset_password_email(user_email, reset_token, user.get("user_first_name", "User"))

            return "Check your email for reset link!"

        except Exception as ex:
            ic(ex)
            return str(ex), 400

        finally:
            if "cursor" in locals(): cursor.close()
            if "db_conn" in locals(): db_conn.close()

##################################
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if request.method == "GET":
        token = request.args.get("token")
        return render_template("reset_password.html", token=token)

    if request.method == "POST":
        try:
            token = request.form.get("token")
            new_password = request.form.get("password")

            if not token or not new_password:
                raise Exception("Token and password required", 400)

            db_conn, cursor = x.db()
            cursor.execute("SELECT reset_expiry FROM users WHERE reset_token=%s", (token,))
            row = cursor.fetchone()

            import datetime
            if not row or datetime.datetime.now() > row["reset_expiry"]:
                raise Exception("Token expired or invalid", 400)

            # Update password + clear token
            from werkzeug.security import generate_password_hash
            cursor.execute(
                "UPDATE users SET user_password=%s, reset_token=NULL, reset_expiry=NULL WHERE reset_token=%s",
                (generate_password_hash(new_password), token)
            )
            db_conn.commit()

            return "Password updated successfully!"

        except Exception as ex:
            ic(ex)
            return str(ex), 400

        finally:
            if "cursor" in locals(): cursor.close()
            if "db_conn" in locals(): db_conn.close()

# api-create-comment
@app.route("/api-create-comment", methods=["POST"])
def api_create_comment():
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    post_fk = request.form.get("post_fk")
    comment_message = request.form.get("comment", "").strip()

    if not post_fk or not comment_message:
        return jsonify({"success": False, "error": "Missing post ID or comment"}), 400

    try:
        db, cursor = x.db()

        comment_pk = uuid.uuid4().hex
        cursor.execute(
            "INSERT INTO comments (comment_pk, comment_post_fk, comment_user_fk, comment_message, created_at) VALUES (%s, %s, %s, %s, NOW())",
            (comment_pk, post_fk, user["user_pk"], comment_message)
        )
        db.commit()

        return jsonify({
            "success": True,
            "comment": {
                "comment_pk": comment_pk,
                "comment_message": comment_message,
                "comment_user_fk": user["user_pk"]
            }
        })

    except Exception as e:
        if "db" in locals(): db.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# Edit comment
@app.route("/api-edit-comment", methods=["POST"])
def api_edit_comment():
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    data = request.get_json()
    comment_pk = data.get("comment_pk")
    new_message = data.get("comment_message", "").strip()

    if not comment_pk or not new_message:
        return jsonify({"success": False, "error": "Missing comment ID or message"}), 400

    try:
        db, cursor = x.db()
        # Ensure only comment owner can edit
        cursor.execute(
            "UPDATE comments SET comment_message = %s WHERE comment_pk = %s AND comment_user_fk = %s",
            (new_message, comment_pk, user["user_pk"])
        )
        db.commit()

        return jsonify({"success": True, "comment_message": new_message})

    except Exception as e:
        if "db" in locals(): db.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

# Delete comment
@app.route("/api-delete-comment", methods=["POST"])
def api_delete_comment():
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "Not logged in"}), 403

    data = request.get_json()
    comment_pk = data.get("comment_pk")
    if not comment_pk:
        return jsonify({"success": False, "error": "Missing comment ID"}), 400

    try:
        db, cursor = x.db()
        # Ensure only comment owner can delete
        cursor.execute(
            "DELETE FROM comments WHERE comment_pk = %s AND comment_user_fk = %s",
            (comment_pk, user["user_pk"])
        )
        db.commit()

        return jsonify({"success": True})

    except Exception as e:
        if "db" in locals(): db.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

