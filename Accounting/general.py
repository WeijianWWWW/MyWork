from dash import Dash,html,dcc 
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
from opreate import add,delete,get_data,month_data,year_data
from datetime import date
import sqlite3
from  login import login_layout
from create import create_layout
from create import create_layout,add_to_db,name_exist
import dash
import json
from add import add_layout
from indival import indival_layout
import plotly.express as px
from all import all_layout
current_user = ' ' 


app = Dash(__name__,suppress_callback_exceptions=True)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
styles = {
'nav-link': {
    'textDecoration': 'none',
    'color': 'white',
    'padding': '5px'
    },
    'nav-link:hover': {
    'textDecoration': 'underline',
    'cursor': 'pointer'
    }
}
today_input_style={
    'height':'40px',
    'width':'500px',
    'background-color':'white',
    'border-radius':'10px',
    'font-size':'12px',
    'margin-left':'0px',
    'margin-top':'5%'
}
today_input=html.Div(
dcc.Input(id='today-input',type='text',value='请输入',style=today_input_style)
)

today_money_input=html.Div(
    dcc.Input(id='today-money',type='text',value='请输入',style=today_input_style)
)

general_layout=html.Div([
    html.Nav([
         html.Ul([
            html.Li(html.A('登陆', href='/login', style=styles['nav-link'])),
            html.Li(html.A('今日记账', href='/general', style=styles['nav-link'])),
            html.Li(html.A('补帐',href='/add',style=styles['nav-link'])),
            html.Li(html.A('我的数据', href='/indival', style=styles['nav-link'])),
            html.Li(html.A('所有数据',href='/all',style=styles['nav-link']))
        ], style={'display': 'flex', 'list-style': 'none', 'margin': 0, 'padding': 0,'gap': '40px'})
    ], style={'background-color': 'rgb(51,105,192)', 'padding': '10px','border-radius':'10px'}),
    html.Div(['请输入今日你想要记录的花费', 
    today_input,
    html.Br(),
    '请输入花费数额',
    today_money_input,
    html.Br(),
    html.Button('提交', id='submit-button', n_clicks=0, 
                style={
                    'backgroundColor': '#0074D9',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'cursor': 'pointer',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'
                }),
                html.Br(),html.Br(),
    html.Button('撤销', id='delete-button', n_clicks=0, 
                style={
                    'backgroundColor': '#0074D9',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'cursor': 'pointer',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'
                }),
    
    ],style={'text-align':'center','margin-left':'5%','margin-top':'5%','width':'90%','border-radius':'10px','box-shadow': '0 4px 8px 0 lightblue',
    'font-size':'30px'}),
    html.Br(),html.Br(),
    html.Div(id='add_stuff_today',children='您即将添加的消费：',style={'background-color':'rgb(51,105,192)','margin-top':'30px','margin-left':'5%',
    'margin-right':'5%','margin-top':'-20px','color':'white','font-size':'15px','border-radius':'10px'}),
    html.Br(),html.Br(),
    html.Div(id='delete_stuff_today',children='您即将删除的消费：',style={'background-color':'rgb(51,105,192)','margin-top':'30px','margin-left':'5%',
    'margin-right':'5%','margin-top':'-20px','color':'white','font-size':'15px','border-radius':'10px'}),
])
    


@app.callback(Output('add_stuff_today','children'),
              Input('submit-button','n_clicks'),
              State('today-input','value'),
              State('today-money','value')
              )
def submit_stuff(n_clicks,stuff_value,money_value):
   current_date = date.today().strftime("%Y-%m-%d")
   if n_clicks != 0:
       add(current_date,stuff_value,money_value,current_user)
       return '您添加了'+' '+current_date+' '+stuff_value+' '+money_value+' '+current_user



@app.callback(Output('delete_stuff_today','children'),
              Input('delete-button','n_clicks')
              )
def delete_stuff(n_clicks):
    if n_clicks !=0:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        query = "SELECT * FROM account ORDER BY rowid DESC LIMIT 1"
        result = cursor.execute(query).fetchone()
        conn.close()
        delete()
        return '删除‘+'+ ' '.join([str(item) for item in result])

@app.callback(Output('page-content', 'children'),
               Input('url', 'pathname'),
               
              )
def display_page(pathname):
    if pathname == '/create':
        return create_layout
    elif pathname == '/general':
        return general_layout
    elif pathname == '/login':
        return login_layout
    elif pathname == '/add':
        return  add_layout
    elif pathname == '/indival':
        return indival_layout
    elif pathname == '/all':
        return all_layout
    else:
        return login_layout


# 回调函数
@app.callback(
    dash.dependencies.Output('login-status', 'children'),
    dash.dependencies.Input('login-button', 'n_clicks'),
    dash.dependencies.State('username', 'value'),
    dash.dependencies.State('password', 'value'),
    dash.dependencies.State('email','value')
)
def authenticate(n_clicks, username, password,email):
    # 检查点击次数
    global current_user
    if n_clicks is None:
     return ''
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE username=? AND password=? AND email=?', (username, password,email))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
         current_user = username
         return html.Div([html.Div('成功登录'),dcc.Link('点击进入下一个页面',href='/general',style={
            'margin': '10px', 
            'color': 'white',
            'backgroundColor': 'lightblue',
            'fontSize': '18px',
            'display': 'block',
            'textAlign': 'center',
            'color': '#333',
            'textDecoration': 'none',
        })])
    return '无效的用户名和密码'



    
@app.callback(
    Output('registration-status', 'children'),
    [Input('register-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value'), State('email', 'value')]
)
def register_user(n_clicks, username, password, email):
    if not username or not password or not email:
        return '请输入有效信息'
    # Check if the username is already taken
    if name_exist(username):
        return '该账号已经注册'
    # Add the new user to the database
    add_to_db(username, password, email)
    return '成功注册'

@app.callback(Output('delete_stuff_otherday','children'),
              Input('otherday_delete_button','n_clicks')
              )
def delete_otherday(n_clicks):
    if n_clicks == 0:
        return ''
    else:
        conn = sqlite3.connect('user.db')
        cursor = conn.cursor()
        query = "SELECT * FROM account ORDER BY rowid DESC LIMIT 1"
        result = cursor.execute(query).fetchone()
        conn.close()
        delete()
        return '删除‘+'+ ' '.join([str(item) for item in result])
    
@app.callback(Output('add_stuff_otherday','children'),
              Input('otherday_submit_button','n_clicks'),
              State('year-dropdown','value'),
              State('month-dropdown','value'),
              State('date-dropdown','value'),
              State('other_input','value'),
              State('other_input_money','value'))
def add_otherday(n_clicks,value1,value2,value3,input_stuff,input_money):
    if n_clicks == 0:
        return ' '
    else: 
        current_time = value1+"-"+value2+"-"+value3

        add(current_time,input_stuff,input_money,current_user)
        return '您添加了'+' '+current_time+' '+input_stuff+' '+input_money+' '+current_user


@app.callback(Output('day_graph','figure'),
              Input('sure_button','n_clicks'),
              State('year','value'),
              State('month','value'),
              State('date','value') 
              )
def draw_inidival(n_clicks,year,month,date):
     time =year+"-"+month+"-"+date
     if n_clicks == 0:
         return ''
     else:
          data = get_data(time,current_user)    # 这是一个list类型数据，其中每个元素是一个元组
          if len(data) == 0:
              return px.bar(x=[0],y=[0],title='没有检测到输入数据')
          stuff = [] 
          money = []
          for tup in data:
              stuff.append(tup[0])
              money.append(tup[1])
          fig = px.bar(x=stuff, y=money, title='日分析')
          print(stuff)
          print(money)
          print(current_user)
          return fig 
     
@app.callback(Output('month_graph','figure'),
              Input('month_button','n_clicks'),
              Input('year','value'),
              Input('month','value')
              )
def  month_draw(n_clicks,year,month):
    if n_clicks == 0:
        return ''
    else:
        time = year+'-'+month
        data = month_data(time, current_user)
        if len(data) == 0:
              return px.bar(x=[0],y=[0],title='没有检测到输入数据')
        keys =list(data.keys())
        moneys = []
        for i in keys:
            moneys.append(data[i])
        fig = px.bar(x = keys,y=moneys,title='月分析')
        return fig
    
@app.callback(Output('year_graph','figure'),
              Input('year_button','n_clicks'),
              Input('year','value'))
def darw_month(n_clicks,year):
    if n_clicks == 0:
        return ''    
    else: 
        time = year
        data = year_data(time,current_user)
        if len(data) == 0:
            return px.bar(x=[0],y=[0],title='没有检测到输入数据')
        keys = list(data.keys())
        moneys = []
        for i in keys:
            moneys.append(data[i])
        fig = px.bar(x =keys, y= moneys, title='年分析')
        return fig  

@app.callback(Output('all-year','figure'),
              Input('user-dropdown','value'),
              Input('year-dropdown','value'),
)             
def get_allyear(user,year):
    if year == None:
        return px.bar(x=[0],y=[0],title='没有检测到输入数据')
    time = year 
    data = year_data(time,user)
    if len(data) == 0:
            return px.bar(x=[0],y=[0],title='没有检测到输入数据')
    keys = list(data.keys())
    moneys = []
    for i in keys:
            moneys.append(data[i])
    fig = px.bar(x =keys, y= moneys, title='当年分析')
    return fig  

@app.callback(Output('all-month','figure'),
              Input('user-dropdown','value'),
              Input('year-dropdown','value'),
              Input('month-dropdown','value'))
def get_allmonth(user,year,month):
    if year == None:
        return px.bar(x=[0],y=[0],title='没有检测到输入数据')
    if month == None:
        return px.bar(x=[0],y=[0],title='没有检测到输入数据')
    
    time = year+'-'+month
    data = month_data(time,user)
    if len(data) == 0:
              return px.bar(x=[0],y=[0],title='没有检测到输入数据')
    keys =list(data.keys())
    moneys = []
    for i in keys:
            moneys.append(data[i])
    fig = px.bar(x = keys,y=moneys,title='当月分析')
    return fig


if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=False)