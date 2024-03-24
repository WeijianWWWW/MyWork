import dash
import dash_auth
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
import sqlite3
from create import create_layout,add_to_db,name_exist
app = dash.Dash(__name__,suppress_callback_exceptions=True)
# 定义数据库连接

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

login_layout = html.Div([
    html.Div([
        html.H1('登录账号', style={'textAlign': 'center', 'color': '#333', 'margin': '0px'})
    ], style={'backgroundColor': '#f2f2f2', 'padding': '20px'}),
    
    html.Div([
        html.Label('用户名', style={'fontWeight': 'bold', 'fontSize': '16px', 'color': '#333'}),
        dcc.Input(id='username', type='text', value='', style={'margin': '10px'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    
    html.Div([
        html.Label('密码', style={'fontWeight': 'bold', 'fontSize': '16px', 'color': '#333'}),
        dcc.Input(id='password', type='password', value='', style={'margin': '10px'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    
    html.Div([
        html.Label('邮箱', style={'fontWeight': 'bold', 'fontSize': '16px', 'color': '#333'}),
        dcc.Input(id='email', type='email', value='', style={'margin': '10px'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}),
    
    html.Button(
        id='login-button', 
        children='登录', 
        style={
            'margin': '20px', 
            'backgroundColor': '#4CAF50', 
            'color': 'white',
            'border': 'none',
            'padding': '10px 20px',
            'borderRadius': '5px',
            'cursor': 'pointer',
            'transition': 'background-color 0.3s ease',
            'margin-left': '46%'
        }
    ),

    dcc.Link(
        '点击进行用户注册',
        href='/create', 
        style={
            'margin': '10px', 
            'color': 'white',
            'backgroundColor': '#4CAF50',
            'fontSize': '18px',
            'display': 'block',
            'textAlign': 'center',
            'color': '#333',
            'textDecoration': 'none',
        }
    ),
    
    html.Div(id='login-status', style={'padding': '20px', 'textAlign': 'center'})
], style={'width': '50%', 'margin': 'auto', 'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)', 'borderRadius': '10px', 'overflow': 'hidden'},id='login-content')



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
    if n_clicks is None:
     return ''
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE username=? AND password=? AND email=?', (username, password,email))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return f'成功登录!'
    return '无效的用户名和密码'

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/create':
        return create_layout
    else:
        return login_layout
    
@app.callback(
    Output('registration-status', 'children'),
    [Input('register-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value'), State('email', 'value')]
)
def register_user(n_clicks, username, password, email):
    print(username)
    if not username or not password or not email:
        return '请输入有效信息'
    # Check if the username is already taken
    if name_exist(username):
        return '您已经完成注册'
    # Add the new user to the database
    add_to_db(username, password, email)
    return '成功注册'



if __name__ == '__main__':
    app.run_server(debug=True)
