import sqlite3
import pandas as pd

conn =  sqlite3.connect('user.db')
query = "select * from account"
df = pd.read_sql_query(query,conn)

conn.close()
df.to_excel('current1.xlsx',index= False)
