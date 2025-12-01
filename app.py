from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import uuid
user_verification_key = uuid.uuid4().hex

from markupsafe import escape
import re

import hashlib
import base64

def verify_scrypt_password(stored, provided):
    # stored example: scrypt:N:r:p$salt$hash
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
@app.route("/admin_login", methods=["GET", "POST"])
@app.route("/admin_login/<lan>", methods=["GET", "POST"])
@x.no_cache
def admin_login(lan="english"):
    import re
    from markupsafe import escape
    import traceback

    # --- Language handling ---
    if lan not in getattr(x, "allowed_languages", []):
        lan = "english"
    x.default_language = lan

    # --- GET request ---
    if request.method == "GET":
        if session.get("admin"):
            return redirect(url_for("admin"))
        return render_template("admin_login.html", lan=lan)

    # --- POST request ---
    if request.method == "POST":
        try:
            print("Admin login POST received")

            # --- Read and sanitize input ---
            admin_email = escape(request.form.get("admin_email", "").strip())
            admin_password = request.form.get("admin_password", "").strip()
            print(f"Email: {admin_email}, Password length: {len(admin_password)}")

            if not admin_email or not admin_password:
                raise Exception("Missing email or password", 400)

            # --- Validate email format ---
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, admin_email):
                raise Exception("Invalid email format", 400)

            # --- Connect to DB ---
            print("Connecting to DB...")
            db, cursor = x.db()
            print("DB connected")

            cursor.execute("SELECT * FROM admin WHERE admin_email=%s", (admin_email,))
            admin = cursor.fetchone()
            print("Admin fetched:", admin)

            if not admin:
                raise Exception("Admin not found", 400)

            # --- Check password hash ---
            if not check_password_hash(admin.get("admin_password", ""), admin_password):
                raise Exception("Invalid credentials", 400)

            # --- Remove password for session ---
            admin.pop("admin_password", None)
            session["admin"] = admin
            print("Admin logged in successfully:", session["admin"])

            return """<browser mix-redirect="/admin"></browser>"""

        except Exception as ex:
            traceback.print_exc()
            code = 400 if len(ex.args) > 1 and ex.args[1] == 400 else 500
            msg = ex.args[0] if code == 400 else "System error, check logs"
            toast_error = render_template("___toast_error.html", message=msg)
            return f"""<browser mix-update="#toast">{toast_error}</browser>""", code

        finally:
            if "cursor" in locals(): cursor.close()
            if "db" in locals(): db.close()

##############################
@app.get("/admin")
@x.no_cache
def admin():
    try:
        admin = session.get("admin")
        if not admin:
            return redirect(url_for("admin_login"))

        db, cursor = x.db()

        # Fetch users
        cursor.execute("SELECT user_pk, user_email, user_blocked FROM users ORDER BY user_pk")
        users = cursor.fetchall()

        # Fetch posts
        cursor.execute("""
            SELECT posts.post_pk, posts.user_fk, posts.post_blocked, users.user_email
            FROM posts
            JOIN users ON posts.user_fk = users.user_pk
            ORDER BY posts.post_pk
        """)
        posts = cursor.fetchall()

        languages = x.allowed_languages

        return render_template("admin.html", admin=admin, users=users, posts=posts, languages=languages)

    except Exception as ex:
        ic(ex)
        return "System error", 500

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

#####################################
@app.post("/admin/block_user/<user_pk>")
def block_user(user_pk):
    try:
        admin = session.get("admin")
        if not admin:
            return redirect(url_for("admin_login"))

        # Validate UUID
        import uuid
        try:
            user_pk = str(uuid.UUID(user_pk))
        except ValueError:
            return "Invalid user ID", 400

        db, cursor = x.db()
        cursor.execute("SELECT user_blocked, user_email FROM users WHERE user_pk=%s", (user_pk,))
        row = cursor.fetchone()
        if not row:
            return "User not found", 404

        new_status = 0 if row["user_blocked"] else 1
        cursor.execute("UPDATE users SET user_blocked=%s WHERE user_pk=%s", (new_status, user_pk))
        db.commit()

        # Send email
        subject = x.lans("account_status_updated")
        status_text = "unblocked" if new_status == 0 else "blocked"
        message = f"Your account has been {status_text} by the administrator."
        x.send_email(row["user_email"], subject, message)

        return redirect(url_for("admin"))

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()


###############################
@app.post("/admin/block_post/<post_pk>")
def block_post(post_pk):
    try:
        admin = session.get("admin")
        if not admin:
            return redirect(url_for("admin_login"))

        # Validate UUID
        import uuid
        try:
            post_pk = str(uuid.UUID(post_pk))
        except ValueError:
            return "Invalid post ID", 400

        db, cursor = x.db()
        cursor.execute("""
            SELECT post_blocked, users.user_email
            FROM posts
            JOIN users ON posts.user_fk = users.user_pk
            WHERE post_pk=%s
        """, (post_pk,))
        row = cursor.fetchone()
        if not row:
            return "Post not found", 404

        new_status = 0 if row["post_blocked"] else 1
        cursor.execute("UPDATE posts SET post_blocked=%s WHERE post_pk=%s", (new_status, post_pk))
        db.commit()

        subject = x.lans("post_status_updated")
        status_text = "unblocked" if new_status == 0 else "blocked"
        message = f"Your post has been {status_text} by the administrator."
        x.send_email(row["user_email"], subject, message)

        return redirect(url_for("admin"))

    finally:
        if "cursor" in locals(): cursor.close()
        if "db" in locals(): db.close()

#############################
@app.get("/admin_logout")
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
            if not check_password_hash(user["user_password"], user_password):
                # Optional: track failed login attempts here for rate-limiting
                raise Exception(dictionary.invalid_credentials[lan], 400)

            # --- Check email verification ---
            if user.get("user_verification_key", "") != "":
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
        email_html = render_template(
            "_email_verify_account.html",
            user_verification_key=user_verification_key
        )
        x.send_email(user_email, "Verify your account", email_html)

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
        ic(tweets)

        html = render_template("_home_comp.html", tweets=tweets)
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

# ###############################
# CREATE POST
# ###############################
@app.route("/api-create-post", methods=["POST"])
def api_create_post():
    db = cursor = None
    try:
        # ---------------- User check ----------------
        user = session.get("user")
        if not user:
            return jsonify({"success": False, "error": "User not logged in"}), 403
        user_pk = user["user_pk"]

        # ---------------- Text ----------------
        post_text = request.form.get("post", "").strip()
        if post_text:
            try:
                post_text = x.validate_post(post_text)
            except Exception:
                pass  # fallback validation

            if len(post_text) < 1 or len(post_text) > 5000:
                return jsonify({"success": False, "error": "Post must be 1-5000 characters"}), 400

        # ---------------- File ----------------
        post_image_path = ""
        file = request.files.get("post_image")
        if file and file.filename:
            if allowed_file(file.filename):
                # Make filename unique
                filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                try:
                    file.save(file_path)
                    post_image_path = filename
                except Exception as e:
                    return jsonify({"success": False, "error": f"File save failed: {str(e)}"}), 500
            else:
                return jsonify({"success": False, "error": "File type not allowed"}), 400

        # ---------------- Validate content ----------------
        if not post_text and post_image_path == "":
            return jsonify({"success": False, "error": "Cannot post empty content"}), 400

        # ---------------- Insert into DB ----------------
        post_pk = uuid.uuid4().hex
        db, cursor = x.db()
        cursor.execute(
            """
            INSERT INTO posts (post_pk, post_user_fk, post_message, post_total_likes, post_image_path, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
            """,
            (post_pk, user_pk, post_text, 0, post_image_path)
        )
        db.commit()

        # ---------------- Prepare HTML ----------------
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
        toast_ok = render_template("___toast_ok.html", message="The world is reading your post!")

        return f"""
            <browser mix-bottom="#toast">{toast_ok}</browser>
            <browser mix-top="#posts">{html_post}</browser>
            <browser mix-replace="#post_container">{html_post_container}</browser>
        """

    except Exception as ex:
        if db: db.rollback()
        traceback.print_exc()
        return jsonify({"success": False, "error": str(ex)}), 500

    finally:
        if cursor: cursor.close()
        if db: db.close()

# ###############################
# UPDATE POST
# ###############################
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

        # Check if post exists and belongs to user
        cursor.execute("SELECT post_user_fk FROM posts WHERE post_pk=%s", (post_pk,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"success": False, "error": "Post not found"}), 404
        if row["post_user_fk"] != user["user_pk"]:
            return jsonify({"success": False, "error": "Not authorized"}), 403

        # Safe to update
        cursor.execute(
            "UPDATE posts SET post_message=%s WHERE post_pk=%s AND post_user_fk=%s",
            (new_text, post_pk, user["user_pk"])
        )
        db.commit()

        return jsonify({"success": True, "post_message": new_text})

    except Exception as e:
        if "db" in locals(): db.rollback()
        traceback.print_exc()
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

@app.route("/api-create-comment/<post_fk>", methods=["POST"])
def api_create_comment(post_fk):
    try:
        user = session.get("user")
        if not user:
            return jsonify({"status": "error", "message": "Invalid user"}), 401

        comment_text = x.validate_comment(request.form.get("comment_text", ""))
        comment_pk = uuid.uuid4().hex
        comment_created_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        db, cursor = x.db()
        cursor.execute(
            "INSERT INTO comments (comment_pk, comment_text, post_fk, user_fk, comment_created_at) VALUES (%s, %s, %s, %s, %s)",
            (comment_pk, comment_text, post_fk, user["user_pk"], comment_created_at)
        )
        db.commit()

        return jsonify({
            "status": "ok",
            "user_first_name": user.get("user_first_name"),
            "user_last_name": user.get("user_last_name")
        })

    except Exception as ex:
        ic(ex)
        return jsonify({"status": "error", "message": "Server error"}), 500

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

        # Prevent duplicates
        cursor.execute(
            "SELECT 1 FROM follows WHERE follow_follower_fk=%s AND follow_following_fk=%s LIMIT 1",
            (user["user_pk"], following_pk)
        )
        if cursor.fetchone():
            return jsonify({"success": True})  # Already following

        follow_pk = uuid.uuid4().hex
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


# DELETE USER
@app.post("/delete-user")
def delete_user():
    user_pk = request.form.get("user_pk")

    # Validate user ID
    if not user_pk or not user_pk.isdigit():
        return "Invalid user ID", 400

    db, cursor = x.db()

    try:
        # Fetch avatar path
        cursor.execute(
            "SELECT user_avatar_path FROM users WHERE user_pk = %s",
            (user_pk,)
        )
        row = cursor.fetchone()

        # Delete user avatar file if it exists
        if row:
            avatar_path = row.get("user_avatar_path")
            if avatar_path:
                full_path = os.path.join("static", avatar_path)
                if os.path.isfile(full_path):
                    os.remove(full_path)

        # Delete user from DB
        cursor.execute("DELETE FROM users WHERE user_pk = %s", (user_pk,))
        db.commit()

        return redirect(url_for("home"))

    except Exception as ex:
        db.rollback()
        print("Error deleting user:", ex)
        return "An error occurred while deleting the user", 500

    finally:
        cursor.close()
        db.close()
