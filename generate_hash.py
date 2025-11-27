from werkzeug.security import generate_password_hash

plain_password = "password"
hashed_password = generate_password_hash(plain_password)
print(hashed_password)
