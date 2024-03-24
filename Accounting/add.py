from dash import Dash,html,dcc 
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
from opreate import add,delete
from datetime import date
import sqlite3
import dash
import json
import datetime
import calendar

app =Dash(__name__)
current_year = datetime.datetime.now().year
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

add_layout= html.Div([
html.Nav([
         html.Ul([
            html.Li(html.A('登陆', href='/login', style=styles['nav-link'])),
            html.Li(html.A('今日记账', href='/general', style=styles['nav-link'])),
            html.Li(html.A('补帐',href='/add',style=styles['nav-link'])),
            html.Li(html.A('我的数据', href='/indival', style=styles['nav-link'])),
            html.Li(html.A('所有数据',href='/all',style=styles['nav-link']))
        ], style={'display': 'flex', 'list-style': 'none', 'margin': 0, 'padding': 0,'gap': '40px'})
    ], style={'background-color': 'rgb(51,105,192)', 'padding': '10px','border-radius':'10px'}),

    html.Div(['请在这里添加没有记录的消费数据',
             html.H4('请选择年份',style={'margin-left':'-85%'}),
             dcc.Dropdown(
             id = 'year-dropdown',
             options=year,
             value='2023',
             style={'color':'black','height':'40px','margin-left':'0%','width':'200px','font-size':'10px','margin-top':'30px'}
             ),
          
             html.H4('请选择月份',style={'margin-left':'-85%'}),
             dcc.Dropdown(
             id = 'month-dropdown',
             options = months,
             value= '01',
             style= {'color':'black','height':'40px','width':'200px','font-size':'10px','text-align':'center','position':'flex','margin-top':'20px'}
             ),

             html.H4('请选择日期',style={'margin-left':'-85%'}),
             dcc.Dropdown(
             id = 'date-dropdown',
             options= days,
             value= '01',
             style=  {'color':'black','height':'40px','width':'200px','font-size':'10px','text-align':'center','position':'flex','margin-top':'20px'}
             ),
             
             html.H4('请输入你想要添加的花费',style={'margin-top':'-440px','margin-left':'200px'}),
             dcc.Input('',id='other_input',style={'border-radius':'10px','border':'none','margin-top':'0px','position':'absolute','width':'500px','height':'30px','margin-left':'-100px'}),
    
             html.H4('请输入你的消费数目',style={'margin-top':'100px','margin-left':'150px'}),
             dcc.Input('',id='other_input_money',style={'border-radius':'10px','border':'none','margin-top':'0px','position':'absolute','width':'500px','height':'30px','margin-left':'30px'}),

             html.Button('提交', id='otherday_submit_button', n_clicks=0, 
                style={
                    'backgroundColor': '#0074D9',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'cursor': 'pointer',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
                    'margin-top':'100px',
                    'margin-left':'70px',
                    'position':'absolute'
                }),

             html.Button('撤销', id='otherday_delete_button', n_clicks=0, 
                style={
                    'backgroundColor': '#0074D9',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '5px',
                    'padding': '10px 20px',
                    'fontSize': '16px',
                    'fontWeight': 'bold',
                    'cursor': 'pointer',
                    'boxShadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
                    'margin-top':'100px',
                    'margin-left':'200px'
                }),
             
     html.Div(id='add_stuff_otherday',children='您即将添加的消费：',style={'background-color':'rgb(51,105,192)','margin-top':'100px','margin-left':'5%',
    'margin-right':'5%','color':'white','font-size':'15px','border-radius':'10px'}),
    html.Br(),html.Br(),
    html.Div(id='delete_stuff_otherday',children='您即将删除的消费：',style={'background-color':'rgb(51,105,192)','margin-top':'30px','margin-left':'5%',
    'margin-right':'5%','margin-top':'-20px','color':'white','font-size':'15px','border-radius':'10px'}),


    ],style={'width':'1000px','height':'800px','border-radius':'10px','background-color':'lightblue','margin-left':'20%',
                    'margin-top':'3%','text-align':'center','font-size':'30px','color':'white'})
])

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
        add(current_time,input_stuff,input_money)
        return '您添加了'+' '+current_time+' '+input_stuff+' '+input_money


app.layout = add_layout

if __name__ == '__main__':
    app.run_server(debug = True)