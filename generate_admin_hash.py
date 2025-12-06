from werkzeug.security import generate_password_hash

# Dit ønskede admin password
plain_password = "SuperSecretAdmin123"  # <-- choose your admin password

# Generér hash
hashed_password = generate_password_hash(plain_password)

# Print hash til brug i databasen
print(hashed_password)
