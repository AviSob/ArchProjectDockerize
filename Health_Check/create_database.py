import sqlite3

conn = sqlite3.connect('health.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE health
          (log_id INTEGER PRIMARY KEY ASC, 
           service VARCHAR(250) NOT NULL,
           status VARCHAR(250) NOT NULL,
           time_stamp VARCHAR(250) NOT NULL)
          ''')

conn.commit()
conn.close()