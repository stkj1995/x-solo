from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

user_password = request.form["user_password"]
hashed_password = generate_password_hash(user_password)  # this produces a string like your DB value

import uuid
user_verification_key = uuid.uuid4().hex

import gspread
import requests
import json
import time
import uuid
import x 
import dictionary
import io
import csv
import traceback
from werkzeug.utils import secure_filename
import datetime

from oauth2client.service_account import ServiceAccountCredentials

from icecream import ic
ic.configureOutput(prefix=f'----- | ', includeContext=True)

app = Flask(__name__)
app.config["DEBUG"] = True

# Set the maximum file size to 10 MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024   # 1 MB

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

import os
from werkzeug.utils import secure_filename

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

##############################
@app.route("/login", methods=["GET", "POST"])
@app.route("/login/<lan>", methods=["GET", "POST"])
@x.no_cache
def login(lan = "english"):

    if lan not in x.allowed_languages: lan = "english"
    x.default_language = lan

    if request.method == "GET":
        if session.get("user", ""): return redirect(url_for("home"))
        return render_template("login.html", lan=lan)

    if request.method == "POST":
        try:
        
            # Validate           
            ic(request.form)  # Se hvad der faktisk bliver sendt
            user_email = x.validate_user_email(lan)
            user_password = x.validate_user_password(lan)
            ic(user_email, user_password)
            # Connect to the database
            q = "SELECT * FROM users WHERE user_email = %s"
            db, cursor = x.db()
            cursor.execute(q, (user_email,))
            user = cursor.fetchone()
            if not user: raise Exception(dictionary.user_not_found[lan], 400)

            if not check_password_hash(user["user_password"], user_password):
                raise Exception(dictionary.invalid_credentials[lan], 400)

            # if user["user_verification_key"] != "":
            #     raise Exception(dictionary.user_not_verified[lan], 400)
            
            ic("user_verification_key:", user["user_verification_key"])

            user.pop("user_password")

            session["user"] = user
            ic(user)
            ic(request.form)
            return f"""<browser mix-redirect="/home"></browser>""", 200

        except Exception as ex:
            ic(ex)

            # User errors
            if ex.args[1] == 400:
                toast_error = render_template("___toast_error.html", message=ex.args[0])
                return f"""<browser mix-update="#toast">{ toast_error }</browser>""", 400

            # System or developer error
            toast_error = render_template("___toast_error.html", message="System under maintenance")
            return f"""<browser mix-bottom="#toast">{ toast_error }</browser>""", 500

        finally:
            if "cursor" in locals(): cursor.close()
            if "db" in locals(): db.close()


##############################
@app.route("/signup", methods=["GET", "POST"])
@app.route("/signup/<lan>", methods=["GET", "POST"])
def signup(lan = "english"):

    if lan not in x.allowed_languages: lan = "english"
    x.default_language = lan

    if request.method == "GET":
        return render_template("signup.html", lan=lan)

    if request.method == "POST":
        try:
            # Validate
            user_email = x.validate_user_email()
            user_password = x.validate_user_password()
            user_username = x.validate_user_username()
            user_first_name = x.validate_user_first_name()

            user_pk = uuid.uuid4().hex
            user_last_name = ""
            user_avatar_path = "https://avatar.iran.liara.run/public/40"
            user_verification_key = uuid.uuid4().hex
            user_verified_at = 0

            user_hashed_password = generate_password_hash(user_password)

            # Connect to the database
            q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            db, cursor = x.db()
            cursor.execute(q, (user_pk, user_email, user_hashed_password, user_username, 
            user_first_name, user_last_name, user_avatar_path, user_verification_key, user_verified_at))
            db.commit()
            q = "INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            # send verification email
            email_verify_account = render_template("_email_verify_account.html", user_verification_key=user_verification_key)
            ic(email_verify_account)
            # x.send_email(user_email, "Verify your account", email_verify_account)

            return f"""<mixhtml mix-redirect="{ url_for('login') }"></mixhtml>""", 200

        except Exception as ex:
            ic(ex)
            # User errors
            if ex.args[1] == 400:
                toast_error = render_template("___toast_error.html", message=ex.args[0])
                return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
            
            # Database errors
            if "Duplicate entry" and user_email in str(ex): 
                toast_error = render_template("___toast_error.html", message="Email already registered")
                return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
            if "Duplicate entry" and user_username in str(ex): 
                toast_error = render_template("___toast_error.html", message="Username already registered")
                return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
            
            # System or developer error
            toast_error = render_template("___toast_error.html", message="System under maintenance")
            return f"""<mixhtml mix-bottom="#toast">{ toast_error }</mixhtml>""", 500

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


# HOME #############################
@app.get("/home")
@x.no_cache
def home():
    try:
        user = session.get("user", "")
        if not user: return redirect(url_for("login"))
        db, cursor = x.db()
        q = "SELECT * FROM users JOIN posts ON user_pk = post_user_fk ORDER BY RAND() LIMIT 5"
        cursor.execute(q)
        tweets = cursor.fetchall()
        ic(tweets)

        q = "SELECT * FROM trends ORDER BY RAND() LIMIT 3"
        cursor.execute(q)
        trends = cursor.fetchall()
        ic(trends)

        q = "SELECT * FROM users WHERE user_pk != %s ORDER BY RAND() LIMIT 3"
        cursor.execute(q, (user["user_pk"],))
        suggestions = cursor.fetchall()
        ic(suggestions)

        return render_template("home.html", tweets=tweets, trends=trends, suggestions=suggestions, user=user)
    except Exception as ex:
        ic(ex)
        return "error"
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

# HOME COMP #############################
@app.get("/home-comp")
def home_comp():
    try:

        user = session.get("user", "")
        if not user: return "error"
        db, cursor = x.db()
        q = "SELECT * FROM users JOIN posts ON user_pk = post_user_fk ORDER BY RAND() LIMIT 5"
        cursor.execute(q)
        tweets = cursor.fetchall()

        # attach comments to each post
        for tweet in tweets:
            q_comments = "SELECT comment_text, user_first_name, user_last_name FROM comments JOIN users ON user_pk = user_fk WHERE post_fk = %s ORDER BY comment_created_at ASC"
            cursor.execute(q_comments, (tweet["post_pk"],))
            tweet["comments"] = cursor.fetchall()

        ic(tweets[0])

        html = render_template("_home_comp.html", tweets=tweets, user=user)
        return f"""<mixhtml mix-update="main">{ html }</mixhtml>"""
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        pass

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

# LIKE TWEET #############################
@app.patch("/like-tweet")
@x.no_cache
def api_like_tweet():
    try:
        button_unlike_tweet = render_template("___button_unlike_tweet.html")
        return f"""
            <mixhtml mix-replace="#button_1">
                {button_unlike_tweet}
            </mixhtml>
        """
    except Exception as ex:
        ic(ex)
        return "error"
    finally:
        # if "cursor" in locals(): cursor.close()
        # if "db" in locals(): db.close()
        pass

# API CREATE POST #############################
@app.route("/api-create-post", methods=["POST"])
def api_create_post():
    try:
        # -----------------------------
        # Validate session
        # -----------------------------
        user = session.get("user")
        if not user:
            return "Invalid user", 403
        user_pk = user["user_pk"]

        # -----------------------------
        # Get text (optional)
        # -----------------------------
        post_text = request.form.get("post", "").strip()
        if post_text:
            post_text = x.validate_post(post_text)  # only validate if text exists

        post_pk = uuid.uuid4().hex
        post_image_path = None

        # -----------------------------
        # Handle file upload (optional)
        # -----------------------------
        file = request.files.get("post_image")
        if file and allowed_file(file.filename):
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # Save relative path for templates
            post_image_path = f"uploads/{filename}"
        elif file:
            toast_error = render_template("___toast_error.html", message="File type not allowed")
            return f"<browser mix-bottom='#toast'>{toast_error}</browser>", 400

        # -----------------------------
        # Must have at least text or media
        # -----------------------------
        if not post_text and not post_image_path:
            toast_error = render_template("___toast_error.html", message="Cannot post empty content")
            return f"<browser mix-bottom='#toast'>{toast_error}</browser>", 400

        # -----------------------------
        # Insert into database
        # -----------------------------
        db, cursor = x.db()
        cursor.execute("""
            INSERT INTO posts (post_pk, post_user_fk, post_message, post_total_likes, post_image_path)
            VALUES (%s, %s, %s, %s, %s)
        """, (post_pk, user_pk, post_text, 0, post_image_path))
        db.commit()

        # -----------------------------
        # Render HTML for frontend
        # -----------------------------
        toast_ok = render_template("___toast_ok.html", message="The world is reading your post!")
        tweet = {
            "user_first_name": user["user_first_name"],
            "user_last_name": user["user_last_name"],
            "user_username": user["user_username"],
            "user_avatar_path": user["user_avatar_path"],
            "post_message": post_text,
            "post_pk": post_pk,
            "post_image_path": post_image_path
        }
        html_post_container = render_template("___post_container.html")
        html_post = render_template("_tweet.html", tweet=tweet, user=user)

        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-top="#posts">{html_post}</browser>
            <browser mix-replace="#post_container">{html_post_container}</browser>
        """

    except Exception as ex:
        if "db" in locals(): db.rollback()
        import traceback; traceback.print_exc()
        toast_error = render_template("___toast_error.html", message="System under maintenance")
        return f"<browser mix-bottom='#toast'>{toast_error}</browser>", 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()



# API UPDATE POST ################################
@app.route("/api-update-post/<post_pk>", methods=["POST"])
def api_update_post(post_pk):
    user = session.get("user")
    if not user:
        return jsonify({"success": False, "error": "User not logged in"}), 403

    new_text = request.form.get("post_message", "").strip()
    if not new_text:
        return jsonify({"success": False, "error": "No content provided"}), 400

    try:
        db, cursor = x.db()

        # Debug: print incoming data
        print("Session user:", user)
        print("Updating post_pk:", post_pk)
        print("New text:", new_text)

        # Check if post exists and belongs to user first
        cursor.execute("SELECT post_user_fk FROM posts WHERE post_pk=%s", (post_pk,))
        row = cursor.fetchone()
        print("DB row:", row)

        if not row:
            return jsonify({"success": False, "error": "Post not found"}), 404
        if row["post_user_fk"] != user["user_pk"]:
            return jsonify({"success": False, "error": "Not authorized"}), 403

        # Now safe to update
        cursor.execute(
            "UPDATE posts SET post_message=%s WHERE post_pk=%s AND post_user_fk=%s",
            (new_text, post_pk, user["user_pk"])
        )
        db.commit()
        print("Rows updated:", cursor.rowcount)

        return jsonify({"success": True, "post_message": new_text})

    except Exception as e:
        if "db" in locals(): db.rollback()
        print("Error updating post:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# API DELETE POST #############################
@app.route("/api-delete-post/<post_pk>", methods=["POST"])
def api_delete_post(post_pk):
    try:
        user = session.get("user", "")
        if not user:
            return jsonify({"success": False, "error": "Invalid user"}), 403
        user_pk = user["user_pk"]

        db, cursor = x.db()

        # Check if post exists and belongs to user
        cursor.execute("SELECT post_user_fk FROM posts WHERE post_pk=%s", (post_pk,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "error": "Post not found"}), 404
        if row["post_user_fk"] != user_pk:
            return jsonify({"success": False, "error": "Not authorized"}), 403

        # Delete post
        cursor.execute("DELETE FROM posts WHERE post_pk=%s", (post_pk,))
        db.commit()

        return jsonify({"success": True, "post_pk": post_pk})

    except Exception as ex:
        if "db" in locals(): db.rollback()
        print("Delete post exception:", ex)   # 🔹 DEBUG: print real error
        return jsonify({"success": False, "error": "Error deleting post"}), 500
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# API CREATE POST #############################
@app.route("/api-create-comment/<post_fk>", methods=["POST"])
def api_create_comment(post_fk):
    try:
        user = session.get("user", "")
        if not user:
            return "invalid user"
        user_fk = user["user_pk"] 

        comment_text = x.validate_comment(request.form.get("comment_text", ""))
        
        comment_pk = uuid.uuid4().hex

        comment_created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        db, cursor = x.db()
        cursor.execute(
            "INSERT INTO comments (comment_pk, comment_text, post_fk, user_fk, comment_created_at) VALUES (%s, %s, %s, %s, %s)",
            (comment_pk, comment_text, post_fk, user_fk, comment_created_at)
        )
        db.commit()
        ##toast_ok = render_template("___toast_ok.html", message="Your comment was posted!")
        comment = {
            "user_first_name": user["user_first_name"],
            "user_last_name": user["user_last_name"],
            "user_username": user["user_username"],
            "user_avatar_path": user["user_avatar_path"],
            "comment_text": comment_text,
        }
        ##html_comment_container = render_template("___comment_container.html")
        ##html_comment = render_template("_comment.html", comment=comment)

        # This will reload the whole page when commenting - will have to fix this later by returning JSON instead
        return {"status": "ok"}
        ##return redirect(url_for("home"))
    
     ##return f"""
            ##<browser mix-bottom="#toast">{toast_ok}</browser>
            ##<browser mix-top="#comments">{html_comment}</browser>
            ##<browser mix-replace="#post_container">{html_comment_container}</browser>
        ##"""
    
    ## Todo
    except Exception as ex:
        ic(ex)
        return "error"
    
    ## Todo
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()    

# API UPDATE PROFILE #############################
@app.route("/api-update-profile", methods=["POST"])
def api_update_profile():

    try:

        user = session.get("user", "")
        if not user: return "invalid user"

        # Validate
        user_email = x.validate_user_email()
        user_username = x.validate_user_username()
        user_first_name = x.validate_user_first_name()

        # Connect to the database
        q = "UPDATE users SET user_email = %s, user_username = %s, user_first_name = %s WHERE user_pk = %s"
        db, cursor = x.db()
        cursor.execute(q, (user_email, user_username, user_first_name, user["user_pk"]))
        db.commit()

        # Response to the browser
        toast_ok = render_template("___toast_ok.html", message="Profile updated successfully")
        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-update="#profile_tag .name">{user_first_name}</browser>
            <browser mix-update="#profile_tag .handle">{user_username}</browser>
            
        """, 200
    except Exception as ex:
        ic(ex)
        # User errors
        if ex.args[1] == 400:
            toast_error = render_template("___toast_error.html", message=ex.args[0])
            return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
        
        # Database errors
        if "Duplicate entry" and user_email in str(ex): 
            toast_error = render_template("___toast_error.html", message="Email already registered")
            return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
        if "Duplicate entry" and user_username in str(ex): 
            toast_error = render_template("___toast_error.html", message="Username already registered")
            return f"""<mixhtml mix-update="#toast">{ toast_error }</mixhtml>""", 400
        
        # System or developer error
        toast_error = render_template("___toast_error.html", message="System under maintenance")
        return f"""<mixhtml mix-bottom="#toast">{ toast_error }</mixhtml>""", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


# API SEARCH #############################
@app.post("/api-search")
def api_search():
    try:
        search_for = request.form.get("search_for", "")
        if not search_for: 
            return "empty search field", 400

        part_of_query = f"%{search_for}%"
        ic(search_for)

        db, cursor = x.db()

        # Search users by username or first name
        q_users = """
        SELECT * FROM users 
        WHERE user_username LIKE %s OR user_first_name LIKE %s
        """
        cursor.execute(q_users, (part_of_query, part_of_query))
        users = cursor.fetchall()

        # Search posts
        q_posts = "SELECT * FROM posts WHERE post_message LIKE %s"
        cursor.execute(q_posts, (part_of_query,))
        posts = cursor.fetchall()

        return jsonify({
            "users": users,
            "posts": posts
        })

    except Exception as ex:
        ic(ex)
        return str(ex)
    
    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


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

# API FOLLOW ###########################
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

        # Prevent duplicates
        cursor.execute(
            "SELECT 1 FROM follows WHERE follow_follower_fk=%s AND follow_following_fk=%s LIMIT 1",
            (user["user_pk"], following_pk)
        )
        if cursor.fetchone():
            return jsonify({"success": True})  # Already following

        follow_pk = uuid.uuid4().hex

        # Insert follow
        cursor.execute(
            "INSERT INTO follows (follow_pk, follow_follower_fk, follow_following_fk) VALUES (%s, %s, %s)",
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



# API UNFOLLOW ###########################
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
            "DELETE FROM follows WHERE follow_follower_fk=%s AND follow_following_fk=%s",
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
