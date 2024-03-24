import sqlite3
import dash
import dash_auth
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
def add_to_db(unsername,password,email):
    db = sqlite3.connect('user.db')
    cursor = db.cursor()
    cursor.execute('INSERT INTO user VALUES(?, ?, ?)',(unsername,password,email))
    db.commit()
    db.close()

def name_exist(username):
    db = sqlite3.connect('user.db')
    cursor = db.cursor()
    cursor.execute('SELECT username FROM user')
    results = cursor.fetchall()
    usernames = [row[0] for row in results]
    db.close()
    if username in usernames:
        return True
   
    return False

create = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# 创建布局
create_layout = html.Div([
    html.H1('注册账号', style={'textAlign': 'center', 'color': '#2C3E50'}),
    html.Div([
        html.Label('用户名', style={'font-weight': 'bold', 'color': '#2980B9'}),
        dcc.Input(id='username', type='text', value='', style={'margin': '10px'})
    ]),
    html.Div([
        html.Label('密码', style={'font-weight': 'bold', 'color': '#2980B9'}),
        dcc.Input(id='password', type='password', value='', style={'margin': '10px'})
    ]),
    html.Div([
        html.Label('邮箱', style={'font-weight': 'bold', 'color': '#2980B9'}),
        dcc.Input(id='email', type='email', value='', style={'margin': '10px'})
    ]),
    html.Button(id='register-button', children='注册',  style={'backgroundColor': '#0074D9',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'margin-buttom':'20%',
                     'cursor': 'pointer',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)'
                }),
    dcc.Link('返回',href='/login', style={'backgroundColor': '#0074D9',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'cursor': 'pointer',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
                    'margin-left':'30%',
                    'textDecoration': 'none',
                }),

    html.Div(id='registration-status',children=' ', style={'margin': '10px', 'color': '#2C3E50'}),
   


], style={'width': '50%', 'margin': 'auto', 'background-color': '#F4F4F4'})

@create.callback(
    Output('registration-status', 'children'),
    [Input('register-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value'), State('email', 'value')]
)
def register_user(n_clicks, username, password, email):
    if n_clicks == 0:
        return '  '
    if not username or not password or not email:
        return '请输入有效信息'
    # Check if the username is already taken
    if name_exist(username):
        return '该账号已经注册'
    # Add the new user to the database
    add_to_db(username, password, email)
    return '成功注册'

