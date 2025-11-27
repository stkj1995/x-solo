##############################
def send_verify_email(to_email, user_verification_key):
    try:
        # Create a gmail fullflaskdemomail
        # Enable (turn on) 2 step verification/factor in the google account manager
        # Visit: https://myaccount.google.com/apppasswords
        # Copy the key

        # Email and password of the sender's Gmail account
        sender_email = "sophieteinvigkjer@gmail.com"
        password = "" # If 2FA is on, use an App Password instead

        # Receiver email address that isn't connected to a specific email, but
        # if you signup, you'll get a verification email to that specific email that you've used for the new user.
        receiver_email = "{user_email}"
        
        # Create the email message
        message = MIMEMultipart()
        message["From"] = "My company name"
        message["To"] = receiver_email
        message["Subject"] = "Please verify your account"

        # Body of the email
        body = f"""
        <h1 style="font-family: avenir, san-serif">To verify your account, please</h1> 
        <a href="http://127.0.0.1/verify/{user_verification_key}">click here</a>"""
        message.attach(MIMEText(body, "html"))

        # Connect to Gmail's SMTP server and send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")

        return "email sent"
       
    except Exception as ex:
        raise_custom_exception("cannot send email", 500)
    finally:
        pass


    # annsofie was here



    ######## dette er en branch stkj test

    ### dette er en main branch test