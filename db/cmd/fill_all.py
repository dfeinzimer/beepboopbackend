# https://www.tutorialspoint.com/flask/flask_sqlite.htm



import sqlite3



conn = sqlite3.connect('../db/articles.db')
if(conn != None):
  print("Opened articles.db successfully");
  conn.execute("INSERT INTO articles VALUES(null,'The best article ever','This is the best article ever written','A great article!','David Feinzimer','4/7/19', 'dfeinzimer', '4/7/19')")
  conn.execute("INSERT INTO articles VALUES(null,'My great article'     ,'There once was a lightbulb'           ,'Yup, it is true' ,'David Feinzimer','4/2/19', 'dfeinzimer', '4/6/19')")
  conn.commit()
  conn.close()
  print("articles table filled successfully",'\n');
else:
  print("Cannot open articles.db")



conn = sqlite3.connect('../db/comments.db')
if(conn != None):
  print("Opened comments.db successfully");
  conn.execute("INSERT INTO comments VALUES(null,'dfeinzimer','What a great article','4/7/19')")
  conn.commit()
  conn.close()
  print("comments table filled successfully",'\n');
else:
  print("Cannot open comments.db")



conn = sqlite3.connect('../db/tags.db')
if(conn != None):
  print("Opened tags.db successfully");
  conn.execute("INSERT INTO tags VALUES(null,'apples','test.com')")
  conn.execute("INSERT INTO tags VALUES(null,'bananas','test.com')")
  conn.execute("INSERT INTO tags VALUES(null,'corn','test.com')")
  conn.commit()
  conn.close()
  print("tags table filled successfully",'\n');
else:
  print("Cannot open tags.db")



conn = sqlite3.connect('../db/users.db')
if(conn != None):
  print("Opened users.db successfully");
  conn.execute("INSERT INTO users VALUES(null,'test@email.com','93942e96f5acd83e2e047ad8fe03114d','dfeinzimer')")
  conn.commit()
  conn.close()
  print("users table filled successfully",'\n');
else:
  print("Cannot open users.db")
