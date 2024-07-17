# -*- coding: utf-8 -*-
"""
Created on Mon May  6 23:47:20 2024

@author: Gebruiker
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
from config import colors_config, card_config

dash.register_page(__name__)

background_img = 'linear-gradient(to left, rgba(0,0,0,1), rgba(59,11,63,0.9))'
card_title_img = 'linear-gradient(to right, rgba(0,0,0,1), rgba(255,87,51,0.9))'
card_bg_img = 'linear-gradient(to right, rgba(0,0,0,1), rgba(59,11,63,0.9))'
card_bg_img2 = 'linear-gradient(to right, rgba(0,0,0,1), rgba(59,11,63,1))'

# Define a function to create a titled card
def create_titled_card(title, content, color_title, color_card):
    return dbc.Card(
        [
            dbc.CardHeader(title, style={'background-image': color_title, 'color': 'white'}),
            dbc.CardBody(content, style={
                                         'margin-left':'0px',
                                         'border-radius': '10px',
                                         'border':'4px solid #ddd',
                                         'font-size':'16px',
                                         'background-image':color_card,
                                         })
        ]
    )

layout =  html.Div(style={'background-image': background_img, 
                          #'height': '100vh'
                          },
                      children=[
    dbc.Container([
        html.Div(style={'height': '25px'}),
        dbc.Row([
            dbc.Col([
                 create_titled_card('Description',
                                    html.P("The algorithm presented herein represents a sophisticated, data-driven investment fund leveraging advanced AI and Machine Learning algorithms. This fund operates within the realm of US Index Futures, predicting the expansion of the daily range. The algorithm strategically engages both long and short positions to capitalise on market opportunities. ", 
                                                    className='card-text', 
                                                    style={'color':'#95D7E0'},
                                                    ),
                                    card_title_img, card_bg_img),
                
                html.Br(),
                create_titled_card('Objective',
                                   html.P("The primary objective of the fund is to achieve compelling and sustainable returns by employing our pattern-detecting algorithm during the 23 hour a day tradingday. Striving for both attractiveness and sustainability involves striking a balance between maximising returns and minimising risk, achieved through identification of active and inactive periods and sophisticated risk management.",
                                          className='card-text',
                                          style={'color':'#95D7E0'},
                                          ),
                                   card_title_img, card_bg_img),
                html.Br(),
                create_titled_card('Suitability',
                                  html.P("This fund is specifically tailored for investors who (i) seek capital growth through exposure to global equity markets, (ii) are comfortable with a certain level of risk, (iii) acknowledge that their capital is at risk, understanding that the value of their investment may fluctuate both upward and downard.",
                                         className='card-text', 
                                         style={'color': '#95D7E0'}
                                         ),
                                  card_title_img, card_bg_img),
                html.Br(),
                ], xs=12, sm=12, md=5, lg=5, xl=5),

            dbc.Col([
                create_titled_card('DashBoard Interactivity',
                                   html.Div([
                                       html.P("On the Main page you can select a few parameters to find optimal stop-loss values and see how sensitive cost and slippage are for the performance.",
                                              className='card-text',
                                              style={'color': '#FFFFFF'}
                                              ),
                                       html.Hr(),
                                       html.P('Adjust Cutoff to Pause Trading:',
                                              className='card-text',
                                              style={'color': '#FFFFFF', 'font':'bold'}),                                              
                                       html.P('As this strategy is attempting to capture moves out of the established range, statistically after a day with a larger change, it is quite likely to have a day of trading within a range. These days have been identified as poorly performing days. Adjusting this parameter will prevent trading on certain days. The higher the cutoff, the less days we are filtering out.',
                                              className='card-text',
                                              style={'color': '#95D7E0'}),
                                       html.Hr(),
                                       html.P("Adjust Execution Cost:",
                                              className='card-text',
                                              style={'color': '#FFFFFF'}                                              
                                              ),
                                       html.P("Unfortunately trading comes with a cost. Exchange fees, broker commissions etc. Trading Nasdaq Futures is relatively cheap however.",
                                              className='card-text',
                                              style={'color': '#95D7E0'}),
                                       html.Hr(),
                                       html.P("Adjust Slippage:",
                                              className='card-text',
                                              style={'color': '#FFFFFF'}                                              
                                              ),
                                       html.P("There is never a guarantee the execution price is exactly as intented. The slippage is the mismatch between the intended and the actual executed price. Most times there will be no slippage, but at volatile moments during the day slippage may occur. ",
                                              className='card-text',
                                              style={'color': '#95D7E0'}),
                                       ]),
                                   card_title_img, card_bg_img2),

                ], xs=12, sm=12, md=5, lg=5, xl=5),
            
            
            ]),
        
        ]),
    ])

