import mysql.connector

def seed_database():
    print("Seeding database...")

    try:
        db = mysql.connector.connect(
            host="127.0.0.1",   # Localhost
            port=3307,          # Docker mapped port
            user="root",
            password="password",
            database="x"
        )
        cursor = db.cursor()
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
        return

    # Read SQL file
    with open("x.sql", "r", encoding="utf-8") as f:
        sql_commands = f.read()

    # Split commands by semicolon
    statements = [s.strip() for s in sql_commands.split(";") if s.strip()]

    try:
        for statement in statements:
            cursor.execute(statement)
            print("Executed:", statement[:50], "...")
    except mysql.connector.Error as e:
        print("Error executing SQL:", e)

    db.commit()
    cursor.close()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
