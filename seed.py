import mysql.connector

def seed_database():
    print("Seeding database...")

    try:
        db = mysql.connector.connect(
            host="x_mariadb0",  # Docker container name for MariaDB
            user="root",
            password="password",  # your root password
            database="x"
        )
        cursor = db.cursor()
    except mysql.connector.Error as e:
        print("Error connecting to database:", e)
        return

    with open("x.sql", "r", encoding="utf-8") as f:
        sql_commands = f.read()

    try:
        # Execute the full SQL file, multi=True allows multiple statements
        for result in cursor.execute(sql_commands, multi=True):
            print("Executed:", result.statement[:50], "...")
    except mysql.connector.Error as e:
        print("Error executing SQL:", e)

    db.commit()
    cursor.close()
    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
