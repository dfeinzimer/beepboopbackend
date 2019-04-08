# https://www.tutorialspoint.com/flask/flask_sqlite.htm

# This script is not completed nor working yet as of 6:13 PM April 7, 2019

import sqlite3



conn = sqlite3.connect('../db/tags.db')
if(conn != None):
  print("Opened tags.db successfully");
  print(conn.execute("INSERT INTO test VALUES('apples','oranges')"))
  print(conn.commit())
  print('Closing:',conn.close())
  print("tags table filled successfully",'\n');
else:
  print("Cannot open tags.db")
