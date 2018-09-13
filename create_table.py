import sqlite3

conn = sqlite3.connect('MF.db')
#conn.execute('''CREATE TABLE MF_RECORD
            # (DATE       PRIMARY KEY    NOT NULL,
            # MF1       FLOAT    NOT NULL,
            # MF2       FLOAT    NOT NULL,
            # MF3       FLOAT    NOT NULL,
            # MF4       FLOAT    NOT NULL,
            # MF5       FLOAT    NOT NULL,
            # MF6       FLOAT    NOT NULL,
            # MF7       FLOAT    NOT NULL);''')
conn.execute("INSERT INTO MF_RECORD (DATE, MF1, MF2, MF3, MF4, MF5, MF6, MF7) VALUES(?,?,?,?,?,?,?,?)",('12/45/7',78.0,76.0,66.9,8,8,0.7,5.8))
conn.commit()
conn.close()