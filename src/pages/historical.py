# -*- coding: utf-8 -*-
"""
Created on Sun May  5 11:57:57 2024

@author: Gebruiker
"""
import pandas as pd
import numpy as np
import datetime

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash_table
import plotly.express as px
import plotly.graph_objects as go

from config import colors_config, card_config
import helpers as hl

# =============================================================================
# This is the second page the user will see.
# It contains an overview of the results of the running year where nested dbc Rows and Cols are used to control the placement of the components.
# Minimal interactivity on this page, only buttons to choose the year
# It contains a line graph, 2 bar graphs, one historgram and 3 tables
# All elements are placed on a card with cardheader for visually appealing layout
#
# =============================================================================

# Required so the dash multipager will take this page on. As it is the first page we have to add "path='/'"
dash.register_page(__name__)

# downloading data containing all individual stock trades for the running year
#fname = 'dataDT_daash.csv'
fname = 'rty_22_24_dynstop_vol.csv'
#fname = 'RTY_YTD24.csv'
df = pd.read_csv(f'../{fname}', parse_dates = ['datetime'], index_col = 'datetime')
df = df[df.index < '01-01-2025']

#print(df.pnl_best.sum())

pnlcol = 'pnl'
# unlike on the main page we have selected a close to optimal cutoff pnl of 0.6% on the previous trading day
selected_pnl = 0.025
dfD = df.resample('D').agg({pnlcol:'sum'})
dfD = dfD[dfD[pnlcol] != 0]
dfD = dfD[dfD[pnlcol].shift(1) > selected_pnl]
#print(dfD[-30:].pnl_best.sum())
    
# here we exclude all trading days where the previous day was > cutt-off
excluded_dates = dfD.index.normalize()
#print(excluded_dates)
dff = df[~df.index.normalize().isin(excluded_dates)]

# unlike on main page we have select realistic cost and slippage
cost = 0.1/10000
slip = 0.1/(2200)  # divided by value of 1 nasdaq future 
dff['pnl_ac'] = 0
dff['pnl_ac'][dff[pnlcol] != 0] = dff[pnlcol] - cost - slip
dff['cr_ac'] = dff.pnl_ac.cumsum() + 1
dff['pnl_plus'] = dff.pnl_ac * dff.cr_ac
dff['cr_plus'] = dff.pnl_plus.cumsum() + 1
#print(dff.pnl_plus.sum())

# for the dash_table we need to name and id columns
table1_columns = ['Year','Q1','Q2','Q3','Q4']

# for visual effect we use a background image instead of monotonous color
background_img = 'linear-gradient(to left, rgba(0,0,0,1), rgba(59,11,63,1))'
card_title_img = 'linear-gradient(to left, rgba(95,21,101,0.75), rgba(0,0,0,1))'

# Define a function to create a titled card
def create_titled_card(title, content, color, height=None):
    return dbc.Card(
        [
            dbc.CardHeader(title, style={'background-image': color, 'color': 'white'}),
            dbc.CardBody(content, style={})
        ], style={'height': height}
    )


# Here we start with the page layout
layout = html.Div(
            style={
                'background-image': background_img,  # Specify the path to your image file
                'background-size': 'cover',  # Cover the entire container
                'background-position': 'center',  # Center the background image
  #              'height': '100vh',  # Set the height to full viewport height
            },
    children = [
    dbc.Card(
        dbc.CardBody([
            # ROW 1
            dbc.Row([
                dbc.Col([
                    create_titled_card('Choose TimePeriod',
                                           html.Div([
                                               dbc.Button('2022', id='y2022', n_clicks=0, style={'margin-left': '0px'}),
                                               dbc.Button('2023', id='y2023', n_clicks=0, style={'margin-left': '12px'}),
                                               dbc.Button('2024', id='y2024', n_clicks=0, style={'margin-left': '12px'}),
                                               dbc.Button('TOTAL', id='total', n_clicks=0, style={'margin-left': '12px'}),
                                                 ]),
                                           card_title_img),
                    html.Br(),
                    create_titled_card('KPI',
                                               html.Div([
                                                   dbc.Row([
                                                       dbc.Col([
                                                           dbc.Card([
                                                               html.H3(id = 'perf-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('Performance', style={'color':'#1F8094'}),
                                                               html.Br(),                                                           
                                                               html.H3(id = 'winrate-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('% Winning Trades', style={'color':'#1F8094'}),
                                                               html.Br(),
                                                               html.H3(id = 'windays-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('% Winning Days', style={'color':'#1F8094'}),
                                                               html.Br(),
                                                               html.H3(id = 'winmonths-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('% Winning Months', style={'color':'#1F8094'}),
                                                               html.Br(),
                                                               html.H3(id = 'trades-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('Avg Trades per day', style={'color':'#1F8094'}),
                                                               ], style = {'height':'28rem'}),
                                                           ], width = 6),
                                                       dbc.Col([
                                                           dbc.Card([
                                                               html.H3(id ='sharpe-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('Sharpe Ratio', style={'color':'#1F8094'}),
                                                               html.Br(), 
                                                               html.H3(id = 'pr-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('Profit Ratio', style={'color':'#1F8094'}),
                                                               html.Br(),
                                                               html.H3(id = 'dd-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('Max Drawdown', style={'color':'#1F8094'}),
                                                               html.Br(),
                                                               html.H3(id = 'bestday-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('Best Day', style={'color':'#1F8094'}),
                                                               html.Br(),
                                                               html.H3(id = 'worstday-2', className='responsive-histcard-value', style={'font-weight':'bold', 'margin-left':'4px'}),
                                                               html.H6('Worst Day', style={'color':'#1F8094'}),
                                                               ], style = {'height':'28rem'})
                                                           ], width = 6),
                                                       ]),
                                                   ]),                                           
                                               card_title_img),
                    html.Br(),
                    create_titled_card('Distribution Profits of Single Trades',
                                       dcc.Graph(id = 'stripper',
                                                 figure = hl.generate_histo(dff),
                                                 style = {'height':'35vh'}
                                                 ),
                                       card_title_img,
                                       height = '42vh'
                                       )
                    ],  xs=12, sm=12, md=3, lg=3, xl=3),
                dbc.Col([
                    create_titled_card('Historical Performance', dcc.Graph(id='graph-1-2', figure = {}), card_title_img),
                    html.Br(),
                    create_titled_card('Quarterly Overview Growth of Capital', dash_table.DataTable(
                                                            id='table-1-2',
                                                            data=hl.generate_QPtable(dff).to_dict('records'),
                                                            columns=[{'name': col, 'id': col} for col in table1_columns],
                                                            style_header= {'backgroundColor': '#3F1252', 'color': 'white', 'fontWeight': 'bold'},
                                                            style_table = {'borderRadius': '10px', 'border':'4px solid #ddd'},
                                                            style_cell = {
                                                                'color': '#000000',
                                                                'font-family':'sans-serif',
                                                                },
                                                            ), card_title_img), 
                    html.Div(style={'height':'4px'}),
                    create_titled_card('Quarterly Overview Sharpe Ratio', dash_table.DataTable(
                                                            id='table-2-2',
                                                            data=hl.generate_QStable(dff).to_dict('records'),
                                                            columns=[{'name': col, 'id': col} for col in table1_columns],
                                                            style_header= {'backgroundColor': '#3F1252', 'color': 'white', 'fontWeight': 'bold'},
                                                            style_table = {'borderRadius': '10px', 'border':'4px solid #ddd'},
                                                            style_cell = {
                                                                'color': '#000000',
                                                                'font-family':'sans-serif',
                                                                },
                                                            ), card_title_img), 
                    html.Div(style={'height':'4px'}),
                    create_titled_card('Quarterly Overview Max Drawdown', dash_table.DataTable(
                                                            id='table-2-3',
                                                            data=hl.generate_QDDtable(dff).to_dict('records'),
                                                            columns=[{'name': col, 'id': col} for col in table1_columns],
                                                            style_header= {'backgroundColor': '#3F1252', 'color': 'white', 'fontWeight': 'bold'},
                                                            style_table = {'borderRadius': '10px', 'border':'4px solid #ddd'},
                                                            style_cell = {
                                                                'color': '#000000',
                                                                'font-family':'sans-serif',
                                                                },
                                                            ), card_title_img), 
                    
                    ],  xs=12, sm=12, md=5, lg=5, xl=5),

                dbc.Col([
                    create_titled_card('Monthly performance', dcc.Graph(id='graph-2-2', figure = {}), card_title_img),
                    html.Br(),
                    create_titled_card('Weekly performance', dcc.Graph(id='graph-3-2', figure = {}), card_title_img),
                    ],  xs=12, sm=12, md=4, lg=4, xl=4),
                ], className="equal-height", style={"margin-right": "15px", "margin-left": "15px"}),
            # ROW 2
            ], style = {'background-image': background_img,}  # Specify the path to your image file
            ) # CLOSING CARDBODY
        ), # CLOSING CARD
    ] #CLOSING children
    ) #CLOSING DIV

# =============================================================================
# # The Outputs contain the interactive elements, this page has 4 interactive elements,
# # with the kpi card containing 10 interactive values
# # The Inputs are the choices the User can make, which on this page is only time period related,
# # 
# =============================================================================
@callback(
     [
     Output('graph-1-2', 'figure'),
     Output('perf-2', 'children'),
     Output('winrate-2', 'children'),
     Output('windays-2', 'children'),
     Output('winmonths-2', 'children'),
     Output('trades-2', 'children'),
     Output('sharpe-2', 'children'),
     Output('pr-2', 'children'),
     Output('dd-2', 'children'),
     Output('bestday-2', 'children'),
     Output('worstday-2', 'children'),
     Output('graph-2-2', 'figure'),
     Output('graph-3-2', 'figure'),
     ],
     [
     Input('y2022', 'n_clicks'),
     Input('y2023', 'n_clicks'),
     Input('y2024', 'n_clicks'),
     Input('total', 'n_clicks'),
     ],
     )

def update_page1(y2022, y2023, y2024, total):
    
    ctx = dash.callback_context
    button_id = None
    if ctx.triggered:
   #     return dash.no_update
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # Determine date range based on button click

    if button_id == 'y2022':
        start_date = '01-01-2022'
        end_date = '31-12-2022'
        plot_title = '2022'
    elif button_id == 'y2023':
        start_date = '01-01-2023'
        end_date = '31-12-2023'
        plot_title = '2023'
    elif button_id == 'y2024':
        start_date = '01-01-2024'
        end_date = '31-12-2024'
        plot_title = '2024'
    elif button_id == 'total':
        start_date = '01-01-2018'
        end_date = '31-12-2023'
        plot_title = 'Total'
    else:
        start_date = '01-01-2018'
        end_date = '31-12-2023'
        plot_title = 'Total' 

    dfc = dff[(dff.index >= start_date) & (dff.index <= end_date)]
    
    dfc['cr_ac'] = dfc.pnl_ac.cumsum() + 1
    dfc['pnl_plus'] = dfc.pnl_ac * dfc.cr_ac
    dfc['cr_plus'] = dfc.pnl_plus.cumsum() + 1
    print(dfc.pnl_plus.sum())

    # Generating elements on page    
    figln = hl.generate_line_shaded(dfc)  
  
    performance = hl.Performance(dfc.pnl_plus)
    wr = hl.WinRate(dfc.pnl_plus)
    wd = hl.Windays(dfc.pnl_plus)
    wm = hl.Winmonths(dfc.pnl_plus)
    avgtr = hl.AvgTrades(dfc)
    sharpe = hl.Sharpe(dfc.pnl_ac)
    pr = hl.ProfitRatio(dfc.pnl_plus)
    dd = hl.DrawDown(dfc.pnl_ac)
    bestday = hl.MaxWinDay(dfc.pnl_ac)
    worstday = hl.MaxLossDay(dfc.pnl_ac)
    
    bars = hl.generate_monthly_bars(dfc)
    bars2 = hl.generate_weekly_bars(dfc)
    
     # the order of returns should be the same as the order of Output in the callbacks.
    return [figln, performance, wr, wd, wm, avgtr, sharpe, pr, dd, bestday, worstday, bars, bars2 ]