import sqlite3

db = sqlite3.connect('api.db')

cursor = db.cursor()
cursor.execute('''CREATE TABLE tok(
    pi NVARCHAR(100),
    tok NVARCHAR(100),
    stats CHAR(100)
    );
               ''')
db.commit()
db.close