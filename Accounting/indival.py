from dash import Dash,html,dcc 
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
from opreate import add,delete
from datetime import date
import sqlite3
import plotly.graph_objs as go
import pandas as pd
from opreate import get_data
import plotly.express as px
app = Dash(__name__)

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

days = [{'label': f"{i}号     ", 'value': f"{i:02d}"} for i in range(1,32)]

months = [{'label': f"{i}月", 'value': f"{i:02d}"} for i in range(1, 13)]

indival_layout = html.Div([
html.Nav([
         html.Ul([
            html.Li(html.A('登陆', href='/login', style=styles['nav-link'])),
            html.Li(html.A('今日记账', href='/general', style=styles['nav-link'])),
            html.Li(html.A('补帐',href='/add',style=styles['nav-link'])),
            html.Li(html.A('我的数据', href='/indival', style=styles['nav-link'])),
            html.Li(html.A('所有数据',href='/all',style=styles['nav-link']))
        ], style={'display': 'flex', 'list-style': 'none', 'margin': 0, 'padding': 0,'gap': '40px'})
    ], style={'background-color': 'rgb(51,105,192)', 'padding': '10px','border-radius':'10px'}),
        html.Div([
        html.H1('请选择想要展示的时间',style={'margin-left':'-1500px'}),
        
        html.Div([
            html.H4('请选择年份',style={'margin-left':'50px'}),
             dcc.Dropdown(
             id = 'year',
             options=year,
             value='2023',
             style={'color':'black','height':'40px','margin-left':'0%','width':'200px','font-size':'10px','margin-top':'-10px',}
             ),
          
             html.H4('请选择月份',style={'margin-left':'50px'}),
             dcc.Dropdown(
             id = 'month',
             options = months,
             value= '01',
             style= {'color':'black','height':'40px','width':'200px','font-size':'10px','text-align':'center','position':'flex','margin-top':'20px'}
             ),

             html.H4('请选择日期',style={'margin-left':'50px'}),
             dcc.Dropdown(
             id = 'date',
             options= days,
             value= '01',
             style=  {'color':'black','height':'40px','width':'200px','font-size':'10px','text-align':'center','position':'flex','margin-top':'20px'}
             ),
        ],style={'background-color':'rgb(51,105,192)','border-radius':'30px','width':'300px','margin-right':'800px','height':'300px'}),
        html.Button(
        id = 'sure_button',children='展示一天数据',
        style={
            'background-color':'rgb(51,105,192)',
            'width':'200px',
            'height':'50px',
            'color':'white',
            'border-radius':'10px',
            'border': 'none',
            'padding':'5px',
            'margin-top':'100px',
            'font-size':'20px',
            'margin-left':'-1600px',
            'cursor': 'pointer',
            'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
        }
        ),
        html.Button(
        id = 'month_button',children = '展示整月数据',
        style={
            'background-color':'rgb(51,105,192)',
            'width':'200px',
            'height':'50px',
            'color':'white',
            'border-radius':'10px',
            'border': 'none',
            'padding':'5px',
            'margin-top':'200px',
            'font-size':'20px',
            'margin-left':'-200px',
            'cursor': 'pointer',
            'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
            'position':'absolute'
        }
        ),
        html.Button(
        id = 'year_button',children = '展示整年数据',
        style={
            'background-color':'rgb(51,105,192)',
            'width':'200px',
            'height':'50px',
            'color':'white',
            'border-radius':'10px',
            'border': 'none',
            'padding':'5px',
            'margin-top':'300px',
            'font-size':'20px',
            'margin-left':'-200px',
            'cursor': 'pointer',
            'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
            'position':'absolute'
        }
        ),
         
        html.Div([html.H2('当月数据',style={'text-align':'center','color':'white'}),
         dcc.Graph(id='month_graph',style={'width':'800px','margin-left':'100px','margin-top':'00px','height':'400px','position':'absolute'})

        ],style={'background-color':'rgb(51,105,192)','margin-left':'600px','width':'1000px','height':'460px','border-radius':'20px','margin-top':'-500px'}),

        html.Div([
        html.H2('当日数据',style={'text-align':'center','color':'white'}),
        dcc.Graph(id='day_graph',style={'width':'500px','margin-left':'75px','margin-top':'-10px','height':'250px','position':'absolute'})
        ],style={'background-color':'rgb(51,105,192)','border-radius':'10px','height':'300px','margin-left':'300px','width':'650px'}),

        html.Div([
        html.H2("当年数据",style={'text-align':'center','color':'white'},),
         dcc.Graph(id='year_graph',style={'width':'500px','margin-left':'75px','margin-top':'-10px','height':'250px','position':'absolute'})
        ],style={'background-color':'rgb(51,105,192)','border-radius':'10px','height':'300px','margin-left':'1100px','width':'650px','margin-top':'-320px'})
             
        
],style={'box-shadow': '0 4px 8px 0 lightblue','height':'850px','margin-top':'2%','margin-left':'1%','text-align':'center','border-radius':'10px'})

]
)

