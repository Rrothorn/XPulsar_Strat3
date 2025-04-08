# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 11:16:16 2024

@author: Gebruiker
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np
import datetime


#helper functions for metrics
def Performance(pnl):
    """ Calculate the total return """
    return "{:.2%}".format(pnl.sum())
def Sharpe(pnl):
    """ Calculate annualised Sharpe Ratio """
    # Resample the pnl series to daily frequency and sum the values for each day
    pnlD = pnl.resample('D').sum()
    
    # Filter out days with zero profit/loss
    pnlD = pnlD[pnlD != 0]
    
    # Calculate the daily return mean and standard deviation
    daily_return_mean = pnlD.mean()
    daily_return_std = pnlD.std()
    
    # Calculate the annualized Sharpe Ratio
    sharpe = (daily_return_mean * 252) / (daily_return_std * (252 ** 0.5))
    return round(sharpe, 2)

def WinRate(pnl):
    """ Calculate the winners vs the losers """
    winrate = len(pnl[pnl > 0]) / len(pnl[pnl != 0])
    return "{:.2%}".format(winrate)
def ProfitRatio(pnl):
    """ Calculate the average profitable trades vs the average losing trade """
    profitratio = -pnl[pnl > 0].mean() / pnl[pnl < 0].mean()
    return round(profitratio, 2)
def Windays(pnl):
    pnlD = pnl.resample('D').agg({'pnl_plus':'sum'})
    winrate = len(pnlD[pnlD.pnl_plus > 0]) / len(pnlD[pnlD.pnl_plus != 0])
    return "{:.2%}".format(winrate)
def Winmonths(pnl):
    pnlM = pnl.resample('M').agg({'pnl_plus':'sum'})
    winrate = len(pnlM[pnlM.pnl_plus > 0]) / len(pnlM)
    return "{:.2%}".format(winrate)

def DrawDown(pnl):
    """Calculate drawdown, or the max losing streak, given a return series."""
    wealth_index = 1000 * (1 + pnl).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdownser = (wealth_index - previous_peaks) / previous_peaks
    drawdown = drawdownser.min()
    return "{:.2%}".format(drawdown)

def MaxWinDay(pnl):
    """Calculate best day"""
    pnlD = pnl.resample('D').agg({'pnl_plus':'sum'})
    return "{:.2%}".format(pnlD.pnl_plus.max())

def MaxLossDay(pnl):
    """Calculate worst day"""
    pnlD = pnl.resample('D').agg({'pnl_plus':'sum'})
    return "{:.2%}".format(pnlD.pnl_plus.min())

def AvgTrades(df):
    trades = len(df[df.pnl != 0])
    dfD = df.resample('D').agg({'pnl_plus':'sum'})
    dfD = dfD[dfD.pnl_plus != 0]
    days = len(dfD)
    return round(trades/days, 2)

# Define the rounding function
def round_to_quarter(value):
    return round(value * 4) / 4

def calculate_sharp(df):
    sharpe = Sharpe(df)
    return pd.Series({'Sharpe': sharpe})

def calculate_drawdown(df):
    dd = DrawDown(df)
    return pd.Series({'DrawDown': dd})

def datetime_to_quarter_str(date):
    quarter = (date.month - 1) // 3 + 1
    return f'Q{quarter}'


#main and historical page elements

def generate_line_shaded(df):
    # This generates a line plot for the YTD performance or capital growth
    # For visual effect we create a shaded fading area underneath the line by introducing shadow traces.
    # The shadowtraces are layers with ever increasing transparency
    dfD = df.resample('D').agg({'pnl_plus':'sum', 'cr_plus':'last'})
    dfD = dfD[dfD.pnl_plus != 0]
    x = dfD.index
    y = dfD.cr_plus
    
    offset = 0.025
    y_shadow = y-0.03 * (y-1)
    y_shadow2 = y-0.06 * (y-1)
    y_shadow3 = y-0.1 * (y-1)
    y_shadow4 = y-0.15 * (y-1)
    y_shadow5 = y-0.2 * (y-1)
    y_shadow6 = y-0.25 * (y-1)
    y_shadow7 = y-0.3 * (y-1)
    y_shadow8 = y-0.4 * (y-1)
    y_shadow9 = y-0.5 * (y-1)
    # Create the line trace
    line_trace = go.Scatter(
        x=x, y=y,
        mode='lines',
        line=dict(color='#C44003', width=2),
        name='Line',
        )

    # Create the shadow trace
    shadow_trace = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y, y_shadow[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.35)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    )
    
    shadow_trace2 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow, y_shadow2[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.33)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    )
    
    shadow_trace3 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow2, y_shadow3[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.31)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    )
    shadow_trace4 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow3, y_shadow4[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.28)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    )
    shadow_trace5 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow4, y_shadow5[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.25)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    )
    shadow_trace6 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow5, y_shadow6[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.22)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    ) 
    shadow_trace7 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow6, y_shadow7[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.18)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    ) 
    shadow_trace8 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow7, y_shadow8[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.14)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    ) 
    shadow_trace9 = go.Scatter(
        x=np.concatenate([x, x[::-1]]),
        y=np.concatenate([y_shadow8, y_shadow9[::-1]]),
        fill='toself',
        fillcolor='rgba(196, 64, 3, 0.1)',  # Adjust the transparency for fading effect
        line=dict(color='rgba(196, 64, 3, 0)', width=0),
        showlegend=False
    ) 
    # Create the figure
    fig = go.Figure()
    
    # Add the shadow trace first (so it is underneath the line)
    fig.add_trace(shadow_trace9)
    fig.add_trace(shadow_trace8)
    fig.add_trace(shadow_trace7)
    fig.add_trace(shadow_trace6)
    fig.add_trace(shadow_trace5)
    fig.add_trace(shadow_trace4)
    fig.add_trace(shadow_trace3)
    fig.add_trace(shadow_trace2)    
    fig.add_trace(shadow_trace)
    
    # Add the line trace
    fig.add_trace(line_trace)
        
    # Update layout for dark background and double y-axis
    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#FFFFFF',
        font_color='#025E70',
        font_family='verdana',  # Replace with your font family if different
        margin={'l':20, 'r':40, 't':50, 'b':10, 'pad':10},
        title={'text':'<b>Growth of Capital</b>', 'x':0.5, 'y':0.98, 'font':{'size':16}},
        xaxis={'title':'', 'showgrid':False},
        yaxis={
            'title':'Growth',
            'tickformat': '.0%',
            'showgrid':False,
        },
        yaxis2={
            'title':'',  # Secondary y-axis title
            'overlaying':'y',  # Overlay on the same plot
            'side':'right',  # Place on the right side
            'showgrid':False,
            'tickvals': fig.layout.yaxis.tickvals if fig.layout.yaxis.tickvals else None  # Sync tick values
        },
        showlegend=False,
    )
    
    return fig

def generate_weekly_bars(df):
    dfW = df.resample('W').agg({'pnl_plus':'sum'})
    bars = px.bar(dfW, x=dfW.index, y=['pnl_plus'],
                  title='<b>Weekly P/L</b>')
    bars.update_layout(
                        plot_bgcolor= '#000000',
                        paper_bgcolor = '#FFFFFF',
                        font_color = '#5B706F',
                        font_family = 'sans-serif',
                        margin = {'l':20, 'r':40, 't':50, 'b':10, 'pad':10},
                        title = {'x':0.5, 'y':0.98, 'font':{'size':16}},
                        xaxis = {'title':'', 'gridcolor':'#808080'},
                        yaxis = {'title':'P/L', 'tickformat': '.1%', 'gridcolor':'#808080'},
                        showlegend = False
                        )  
    bars.update_traces(marker_color='#9615A0')
    
    return bars

def generate_last20days(df):
    dfD = df.resample('D').agg({'pnl_plus':'sum'})
    dfD = dfD[dfD.pnl_plus != 0]
    dfD = dfD[-20:]
    bars = px.bar(dfD, x=['pnl_plus'], y=dfD.index, orientation='h',
                  title='<b>P/L Last 20 trading days</b>')
    bars.update_layout(
                        plot_bgcolor= '#000000',
                        paper_bgcolor = '#FFFFFF',
                        font_color = '#025E70',
                        font_family = 'Verdana',
                        margin = {'l':20, 'r':40, 't':50, 'b':10, 'pad':10},
                        title = {'x':0.5, 'y':0.98, 'font':{'size':16}},
                        yaxis = {'title':'', 'gridcolor':'#808080'},
                        xaxis = {'title':'P/L', 'tickformat': '.2%', 'gridcolor':'#808080'},
                        showlegend = False,
                        )  
    bars.update_traces(marker_color='#9615A0')
    
    return bars

def generate_monthly_bars(df):
    dfM = df.resample('M').agg({'pnl_plus':'sum'})
    bars = px.bar(dfM, x=dfM.index, y=['pnl_plus'],
                  title='<b>Monthly P/L</b>')
    bars.update_layout(
                        plot_bgcolor= '#000000',
                        paper_bgcolor = '#FFFFFF',
                        font_color = '#025E70',
                        font_family = 'verdana',
                        margin = {'l':20, 'r':40, 't':50, 'b':10, 'pad':10},
                        title = {'x':0.5, 'y':0.98, 'font':{'size':16}},
                        xaxis = {'title':'', 'gridcolor':'#808080'},
                        yaxis = {'title':'P/L', 'tickformat': '.1%', 'gridcolor':'#808080'},
                        showlegend = False
                        )  
    bars.update_traces(marker_color='#9615A0')
    
    return bars

def generate_histo(df):
    df = df[df.pnl_plus != 0]
    fig = px.histogram(df, x='pnl_plus', nbins=80, title='<b>Distribution of Trading Profits</b>')
    fig.update_layout(
                        plot_bgcolor= '#000000',
                        paper_bgcolor = '#FFFFFF',
                        font_color = '#025E70',
                        font_family = 'arial',
                        margin = {'l':20, 'r':40, 't':50, 'b':10, 'pad':10},
                        title = {'x':0.5, 'y':0.98, 'font':{'size':16}},
                        yaxis = {'title':'', 'gridcolor':'#808080'},
                        xaxis = {'title':'P/L', 'tickformat': '.1%', 'gridcolor':'#808080'},
                        showlegend = False,
                        bargap = 0.1,
                        )  
    fig.update_traces(marker_color='#9615A0')
    return fig

def generate_table(df):
    dfc = df[df.pnl_plus != 0][['buy_open','buy_close','sell_open','sell_close', 'pnl_plus']][-100:]
    dfc['B/S'] = 0
    dfc['B/S'][dfc.buy_open == 0] = 'SELL'
    dfc['B/S'][dfc.sell_open == 0] = 'BUY'
    dfc['open'] = 0
    dfc['open'][dfc.buy_open == 0] = dfc.sell_open
    dfc['open'][dfc.sell_open == 0] = dfc.buy_open
    dfc['close'] = 0
    dfc['close'][dfc.buy_open == 0] = dfc.sell_close
    dfc['close'][dfc.sell_open == 0] = dfc.buy_close
    dfc['date'] = dfc.index.date
    
    dftable = dfc[['date','B/S', 'pnl_plus']]
    dftable['pnl_plus'] = dftable['pnl_plus'].map(lambda x: f"{x:.2%}")
    dftable = dftable.rename(columns = {'pnl_plus':'Profit'})
    dftable = dftable.sort_index(ascending=False)
    print(dftable)
    
    return dftable

def generate_QPtable(df):
    #Calculates table for Quarterly performance per Year
    dfQ = df.resample('Q').agg({'pnl_plus':'sum'})
    
    # Extract years and quarters
    dfQ['Year'] = dfQ.index.year
    dfQ.reset_index(inplace=True)
    dfQ['Quarter'] = dfQ['datetime'].apply(datetime_to_quarter_str)

    dfQ['pnl_plus'] = dfQ['pnl_plus'].map(lambda x: f"{x:.2%}")
    
    dftable = dfQ.pivot(index='Year', columns='Quarter', values='pnl_plus')
    dftable.reset_index(inplace=True)

    return dftable

def generate_QStable(df):
    #Calculates table for Quarterly Sharpe per Year
    dfQ = df.resample('Q').agg({'pnl_plus':'sum'})
    dfQ['Sharpe'] = df['pnl_plus'].resample('Q').apply(calculate_sharp)
    # Extract years and quarters
    dfQ['Year'] = dfQ.index.year
    dfQ.reset_index(inplace=True)
    dfQ['Quarter'] = dfQ['datetime'].apply(datetime_to_quarter_str)
    
    dftable = dfQ.pivot(index='Year', columns='Quarter', values='Sharpe')
    dftable.reset_index(inplace=True)

    return dftable

def generate_QDDtable(df):
    #Calculate table for Quarterly Drawdown per year
    dfQ = df.resample('Q').agg({'pnl_ac':'sum'})
    dfQ['DrawDown'] = df['pnl_ac'].resample('Q').apply(calculate_drawdown)
    # Extract years and quarters
    dfQ['Year'] = dfQ.index.year
    dfQ.reset_index(inplace=True)
    dfQ['Quarter'] = dfQ['datetime'].apply(datetime_to_quarter_str)
    print(dfQ)
    dftable = dfQ.pivot(index='Year', columns='Quarter', values='DrawDown')
    dftable.reset_index(inplace=True)
    print(dftable)
    return dftable    

def generate_gauge_yoytarget_model(dfg):
    year = 2025
    target = 0.40
    
    #get current and previous years sales
    start_date = str(year) + '-01-01'
    end_date = str(year) + '-12-31'   
    dfc = dfg[(dfg.index >= start_date) & (dfg.index <= end_date)]
    cur_profit = dfc['pnl_plus'].sum() 
    
    profit_target = target 
    
    if cur_profit/profit_target < 0.75:
        bar_color = '#D318E1'
    elif cur_profit/profit_target > 1.2:
        bar_color = '#3B0B3F'
    else:
        bar_color = '#6A0F71'
    
    #create a Gauge Graph 
    fig_target = go.Indicator(
       domain = {'x': [0, 1], 'y': [0, 0.8]},
       value = cur_profit,
       number={'valueformat': '.2%'},
       mode = "gauge+number",   # also including the delta to show how far off the target we are
#       title = {'text': f'{figln_title} Sales vs Target'},
       delta = {'reference':  profit_target, 'valueformat': '.2%'},
       gauge = {'axis': {'range': [None, 1.35 * target], 'tickformat':',.2%', 'tickvals':[0,0.16,0.48,0.64]},
                'bar': {'color': bar_color},  
        #        'shape':'angular',
                'steps' : [{'range': [0, 1.35 * target], 'color': '#FFFFFF'},],
                'threshold' : {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': profit_target},
                },
       )
  

    return fig_target

def generate_gauge_qoqtarget_model(dfg):
    
    #get current and previous years sales
    start_date = '2025-01-01'
    end_date =  '2025-04-01'   
    dfc = dfg[(dfg.index > start_date) & (dfg.index < end_date)]
    cur_profit = dfc['pnl_plus'].sum() 
    
    profit_target = 0.1 
    
    if cur_profit/profit_target < 0.75:
        bar_color = '#D318E1'
    elif cur_profit/profit_target > 1.2:
        bar_color = '#3B0B3F'
    else:
        bar_color = '#6A0F71'
    
    #create a Gauge Graph 
    fig_target = go.Indicator(
       domain = {'x': [0, 1], 'y': [0, 0.8]},
       value = cur_profit,
       number={'valueformat': '.2%'},
       mode = "gauge+number",   # also including the delta to show how far off the target we are
#       title = {'text': f'{figln_title} Sales vs Target'},
       delta = {'reference':  profit_target, 'valueformat': '.2%'},
       gauge = {'axis': {'range': [None, profit_target * 1.35], 'tickformat':',.2%', 'tickvals':[0,0.04,0.12,0.16]},
                'bar': {'color': bar_color},  
        #        'shape':'angular',
                'steps' : [{'range': [0, profit_target * 1.35], 'color': '#FFFFFF'},],
                'threshold' : {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': profit_target},
                },
       )
  

    return fig_target

def generate_gauge_momtarget_model(dfg):
    
    #get current and previous years sales
    start_date = '2025-03-01'
    end_date =  '2025-04-01'   
    dfc = dfg[(dfg.index > start_date) & (dfg.index < end_date)]
    cur_profit = dfc['pnl_plus'].sum() 
    
    profit_target = 0.033
    
    if cur_profit/profit_target < 0.75:
        bar_color = '#D318E1'
    elif cur_profit/profit_target > 1.2:
        bar_color = '#3B0B3F'
    else:
        bar_color = '#6A0F71'
    
    #create a Gauge Graph 
    fig_target = go.Indicator(
       domain = {'x': [0, 1], 'y': [0, 0.8]},
       value = cur_profit,
       number={'valueformat': '.2%'},
       mode = "gauge+number",   # also including the delta to show how far off the target we are
#       title = {'text': f'{figln_title} Sales vs Target'},
       delta = {'reference':  profit_target, 'valueformat': '.2%'},
       gauge = {'axis': {'range': [None, profit_target * 1.35], 'tickformat':',.2%', 'tickvals':[0,0.02,0.04,0.06]},
                'bar': {'color': bar_color},  
        #        'shape':'angular',
                'steps' : [{'range': [0, profit_target * 1.35], 'color': '#FFFFFF'},],
                'threshold' : {'line': {'color': 'red', 'width': 4}, 'thickness': 0.75, 'value': profit_target},
                },
       )
  

    return fig_target

def generate_gauge_multimodel(df):
    subtitles = [
                'Month',           
                'Quarter',
                'Year',
                ]
    # Create a subplot figure with 2x2 layout, specifying the type as 'indicator'
    multi_gauge = make_subplots(
        rows=3, cols=1,
        subplot_titles=(
            subtitles
            ),
        specs=[
            [{'type': 'indicator'}],
            [{'type': 'indicator'}],
            [{'type': 'indicator'}],
            ],
        vertical_spacing=0.2  # Increase vertical spacing between subplots
    )
    
    # Add gauge plots to the subplots
    for i in range(3):
        row = i+1
        col = 1 
        if row == 1:
            gauge = generate_gauge_momtarget_model(df)
        elif row == 2:
            gauge = generate_gauge_qoqtarget_model(df)
        else:
            gauge = generate_gauge_yoytarget_model(df)
        multi_gauge.add_trace(gauge, row=row, col=col)
    # Update layout to add a main title
    multi_gauge.update_layout(
                        plot_bgcolor= '#000000',
                        paper_bgcolor = '#FFFFFF',
                        font_color = '#025E70',
                        font_family = 'arial',
                        title_text=f"<b>Profit Targets 2024</b>",
                        title_x=0.5,  # Center the main title
                        title_font=dict(
 #               family="Arial",  # Specify the font family
                                size=18,         # Specify the font size
                                color= '#025E70',     # Specify the font color
                                ),
                        margin=dict(t=80)  # Adjust the top margin to make room for the main title
                        )    
    return multi_gauge
