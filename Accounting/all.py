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

conn = sqlite3.connect('user.db')
cursor = conn.cursor()
cursor.execute("SELECT username FROM user")
usernames = cursor.fetchall()
usernames = [username[0] for username in usernames]
usernames.append('所有人')
cursor.close()
conn.close()


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
year = [{'label':'2023','value':'2023'},
        {'label':'2024','value':'2024'},
        {'label':'2025','value':'2025'},
        {'label':'2026','value':'2026'},
        {'label':'2027','value':'2027'},
        {'label':'2028','value':'2028'},
        {'label':'2029','value':'2029'},
        ]

months = [{'label': f"{i}月", 'value': f"{i:02d}"} for i in range(1, 13)]


all_layout = html.Div([
  html.Nav([
         html.Ul([
            html.Li(html.A('登陆', href='/login', style=styles['nav-link'])),
            html.Li(html.A('今日记账', href='/general', style=styles['nav-link'])),
            html.Li(html.A('补帐',href='/add',style=styles['nav-link'])),
            html.Li(html.A('我的数据', href='/indival', style=styles['nav-link'])),
            html.Li(html.A('所有数据',href='/all',style=styles['nav-link']))
        ], style={'display': 'flex', 'list-style': 'none', 'margin': 0, 'padding': 0,'gap': '40px'})
    ], style={'background-color': 'rgb(51,105,192)', 'padding': '10px','border-radius':'10px'}),
  html.Div(['请选择你想要查看的数据',
            html.Div(style={'background-color':'rgb(51,105,192)','width':'300px','height':'40px','margin-left':'20px','border-radius':'10px','color':'white','font-size':'18px','text-align':'left','margin-top':'20px'}),
            html.H6('请选择时间',style={'color':'white','position':'absolute','margin-left':'30px','margin-top':'-30px'}),
            html.Div(style={'box-shadow':'0 4px 8px 0 rgba(0,0,0,0.3)','width':'300px','height':'400px','margin-left':'20px','border-radius':'10px'}),
            html.Div(style={'border-bottom': '1px dashed lightgray','width':'300px','margin-top':'-200px','margin-left':'20px'}),

            html.Div(style={'background-color':'rgb(51,105,192)','width':'450px','height':'40px','margin-left':'450px','margin-top':'-240px','border-radius':'10px'}),
            html.H6('当月数据分析',style={'color':'white','position':'absolute','margin-left':'460px','margin-top':'-30px'}),
            html.Div([dcc.Graph(id='all-month')],style={'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.4)','width':'450px','height':'600px','margin-left':'450px','border-radius':'10px'}),

            html.Div(style={'background-color':'rgb(51,105,192)','width':'450px','height':'40px','margin-left':'1050px','margin-top':'-640px','border-radius':'10px'}),
            html.H6('当年数据分析',style={'color':'white','position':'absolute','margin-left':'1060px','margin-top':'-30px'}),
            html.Div([dcc.Graph(id='all-year')],style={'box-shadow': '0 4px 8px 0 rgba(0,0,0,0.4)','width':'450px','height':'600px','margin-left':'1050px','border-radius':'10px'}),
            
            html.Div([dcc.Dropdown(
             id='year-dropdown',options=year,style={'font-size':'14px','box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)'}
            )],style={'background-color':'white','height':'40px','width':'280px','margin-top':'-500px','margin-left':'30px'}),
            html.H3('请选择年份',style={'margin-left':'-1550px','margin-top':'-120px','color':'rgb(51,105,192)'}),



             html.Div([dcc.Dropdown(
             id='month-dropdown',options=months,style={'font-size':'14px','box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)'}
            )],style={'background-color':'white','height':'40px','width':'280px','margin-top':'250px','margin-left':'30px'}),
            html.H3('请选择月份',style={'margin-left':'-1550px','margin-top':'-120px','color':'rgb(51,105,192)'}),
            
             html.Div(style={'background-color':'rgb(51,105,192)','width':'300px','height':'40px','margin-left':'20px','border-radius':'10px','color':'white','font-size':'18px','text-align':'left','margin-top':'170px'}),
             html.H6('请选择查看人',style={'color':'white','position':'absolute','margin-left':'30px','margin-top':'-30px'}),
             html.Div(style={'box-shadow':'0 4px 8px 0 rgba(0,0,0,0.3)','width':'300px','height':'150px','margin-left':'20px','border-radius':'10px'}),
             html.Div([dcc.Dropdown(
             id='user-dropdown',options=usernames,style={'font-size':'14px','box-shadow': '0 4px 8px 0 rgba(0,0,0,0.2)'}
            )],style={'background-color':'white','height':'40px','width':'280px','margin-top':'-100px','margin-left':'30px'}),

            ],style={'box-shadow': '0 4px 8px 0 lightblue','hright':'800px','margin-top':'2%','margin-left':'1%','height':'800px','text-align':'center',
                                'font-weight': 'bold','font-size':'30px','font-family': 'Arial'}),  
])


