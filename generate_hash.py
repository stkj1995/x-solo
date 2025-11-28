from werkzeug.security import generate_password_hash

# Dit ønskede password
plain_password = "password"

# Generér hashed password
hashed_password = generate_password_hash(plain_password)

# Print hash til brug i databasen
print(hashed_password)
