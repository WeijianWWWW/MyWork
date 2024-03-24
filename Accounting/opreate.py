import sqlite3
import pandas as pd
# conn = sqlite3.connect('user.db')
# cursor = conn.cursor()
# cursor.execute("INSERT INTO account (time,stuff,money) VALUES (? , ?, ?)",('2003','去买菜','10'))
# conn.commit()
# cursor.close()
# conn.close()


def delete():
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM account WHERE ROWID=(SELECT MAX(ROWID) FROM account)")
    conn.commit()
    cursor.close()
    conn.close()

def add(time,stuff,money,username):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO account (time,stuff,money,username) VALUES (? , ?, ?, ?)",(time,stuff,money,username))
    conn.commit()
    cursor.close()
    conn.close()

def get_data(time, username):
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    query = 'SELECT stuff, money FROM account WHERE time=? AND username=?'
    cursor.execute(query, (time, username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def month_data(time,username):
   if username != '所有人': 
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    query = 'SELECT time,stuff,money FROM account WHERE username=?'
    cursor.execute(query,(username,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    var_map = {}
    for i in data:
      if time in i[0]:
          if i[0] in var_map:
              original = var_map[i[0]]
              total = original + i[2]
              var_map[i[0]] = total
          else:
              var_map[i[0]]= i[2]
    return var_map
   else:
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    query = 'SELECT time,money FROM account'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    var_map = {}
    for i in data:
      if time in i[0]:
          if i[0] in var_map:
              original = var_map[i[0]]
              total = original + i[1]
              var_map[i[0]] = total
          else:
              var_map[i[0]]= i[1]
    return var_map



def  year_data(time,username):
 if username != '所有人':
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    query = 'SELECT time,stuff,money FROM account WHERE username=?'
    cursor.execute(query,(username,))
    data = cursor.fetchall() #here the data is the list contains all the tuple that satisfy the user name
    var_map = {}
    for element in data:
        if time in element[0]:
            month = element[0][:7]
            if month in var_map:
                var_map[month] = var_map[month]+element[2]
            else:
                var_map[month] = element[2]
    return var_map
 else:
     conn = sqlite3.connect('user.db')
     cursor = conn.cursor()
     query = 'SELECT time,money FROM account'
     cursor.execute(query)
     data = cursor.fetchall()
     cursor.close()
     conn.close()
     var_map = {}
     var_map = {}
     for element in data:
        if time in element[0]:
            month = element[0][:7]
            if month in var_map:
                var_map[month] = var_map[month]+element[1]
            else:
                var_map[month] = element[1]
     return var_map

# @app.callback(Output('all-month','figure'),
#               Input('user-dropdown','value'),
#               Input('year-dropdown','value'),
#               Input('month-dropdown','value'))
# def get_allmonth(user,year,month):
#     if year or month or user == None:
#          return px.bar(x=[0],y=[0],title='没有检测到输入数据')
#     time = year+'-'+month
#     data = month_data(time,user)
#     if len(data) == 0:
#               return px.bar(x=[0],y=[0],title='没有检测到输入数据')
#     keys =list(data.keys())
#     moneys = []
#     for i in keys:
#             moneys.append(data[i])
#     fig = px.bar(x = keys,y=moneys,title='月分析')
#     return fig
