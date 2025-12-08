# import mysql.connector

# conn = mysql.connector.connect(
#     host="teinvig.mysql.eu.pythonanywhere-services.com",
#     user="teinvig",
#     password="datapassword123",
#     database="teinvig$default"
# )

# cursor = conn.cursor()

# with open("/home/teinvig/x-solo/x_clean.sql", "r") as f:
#     sql = f.read()

# for statement in sql.split(";"):
#     if statement.strip():
#         cursor.execute(statement)

# conn.commit()
# conn.close()
# print("SQL imported successfully!")

