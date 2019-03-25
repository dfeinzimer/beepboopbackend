# https://pythontic.com/database/sqlite/drop%20table

# import the sqlite3 module
import sqlite3

# Connect to the demo database
connection  = sqlite3.connect("database_master.db")

# Get a cursor object
cursor = connection.cursor()

# Execute the DROP Table SQL statement
dropTableStatement = "DROP TABLE users"
cursor.execute(dropTableStatement)

# Close the connection object
connection.close()

print("Database cleaned, please recreate and refill with data")
