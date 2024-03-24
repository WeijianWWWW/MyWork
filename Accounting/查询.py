import sqlite3

# 连接到数据库
conn = sqlite3.connect('user.db')

# 创建一个游标对象
cursor = conn.cursor()

# 执行查询
cursor.execute("select * from  account")
data = cursor.fetchall()

for row in data:
    print(row)


# 关闭连接
conn.close()