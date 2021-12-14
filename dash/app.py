import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

#################### MAP ########################
df_map = pd.read_csv('county_price.csv')
df_map['FIPS'] = df_map['FIPS'].apply(lambda x: str(x).zfill(5))

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig_us = px.choropleth(df_map, geojson=counties, locations='FIPS', color='price',
                        color_continuous_scale="jet", hover_name="county",
                        range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1),
                        scope="usa",
                        title = 'USA gas price by county'
                        )
fig_us.update_traces(marker_line_width=0.1, marker_opacity=0.8)
fig_us.update_geos(showsubunits=True, subunitcolor="black")
fig_us.update_layout(height=600, margin={"r":0,"t":50,"l":0,"b":0})
fig_us.update_layout(title={
        'font_size': 30,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    })

#################### table #########################
tb = pd.read_csv('table.csv')

################## scatter plot ####################
final = pd.read_excel('Final_Scatter.xlsx')
option_labels = ['Gas Tax','Median Income',
                 'Vehicle Registration Number', 
                 'Sales Tax', 'Population',
                 'Oil_Production','Gas Sales' ]
option_values = [ 'Gas_Tax','Median_Income',
                 'Auto', 'Sales_Tax', 
                 'Population','Oil_Production','Gas_Sales']
xaxis_labels = {'Auto':'# of Registered Vehicle',
                   'Sales_Tax' : 'Sales Tax (%/$)',
                    'Gas_Tax' : 'Gas Tax ($/ gallon)',
                    'Population' : 'Population',
                    'Median_Income' : 'Median Income ($)',
               'Oil_Production': 'Crude Oil Production (Thousand Barrels)',
               'Gas_Sales':'Total Gasoline All Sales/Deliveries by Prime Supplier (Thousand Gallons per Day)'}
title_labels = {'Auto':'Number of Registered Vehicle',
                   'Sales_Tax' : 'Sales Tax',
                    'Gas_Tax' : 'Gas Tax',
                    'Population' : 'Population',
                    'Median_Income' : 'Median Income',
                   'Oil_Production': 'Crude Oil Production',
               'Gas_Sales':'Gasoline Sales'}

################ box plot #######################
dt=pd.read_excel("state_price_box.xlsx", sheet_name='9state')
ca=dt[dt['state']=='CA']['price']
co=dt[dt['state']=='CO']['price']
fl=dt[dt['state']=='FL']['price']
ma=dt[dt['state']=='MA']['price']
mn=dt[dt['state']=='MN']['price']
ny=dt[dt['state']=='NY']['price']
oh=dt[dt['state']=='OH']['price']
tx=dt[dt['state']=='TX']['price']
wa=dt[dt['state']=='WA']['price']

fig1 = go.Figure()
fig1.add_trace(go.Box(y=ca, name='California',
                marker_color = 'red'))
fig1.add_trace(go.Box(y=co, name='Colorado',
                marker_color = 'orange'))
fig1.add_trace(go.Box(y=fl, name='Florida',
                marker_color = 'yellow'))
fig1.add_trace(go.Box(y=ma, name='Massachusetts',
                marker_color = 'green'))
fig1.add_trace(go.Box(y=mn, name='Minnesota',
                marker_color = 'lightgreen'))
fig1.add_trace(go.Box(y=ny, name='NeW York',
                marker_color = 'blue'))
fig1.add_trace(go.Box(y=oh, name='Ohio',
                marker_color = 'navy'))
fig1.add_trace(go.Box(y=tx, name='Texas',
                marker_color = 'purple'))
fig1.add_trace(go.Box(y=wa, name='Washington',
                marker_color = 'grey'))
fig1.update_yaxes(nticks=18)
fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)'
)
fig1.update_layout(
    title={
        'text': "Today's gas price",
        'font_size': 30,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

################# time series ##########################
price = pd.read_csv('padd_price_by_year.csv',index_col=0)
production = pd.read_csv('padd_net_production.csv',index_col=0)

################### Layout #########################
app.layout = html.Div([
    html.Div(
        className="app-header",
        children = [
            html.H1('US Gas Price From Past to Today') 
        ] 
    ),
    html.Div(className='app-map-us',
        children=[
            dcc.Graph(
                className= 'map-us-plot',
                id= 'usmap',
                figure = fig_us)]
        ),
    html.Div(className='app-map-state',
        children=[
            dcc.Dropdown(id='map_state_dropdown',
                    options=[{'label': j, 'value': j}
                            for j in df_map.state.unique()],
                    value = 'CA'),
            dcc.Graph(
                className= 'map-state-plot',
                id= 'statemap')
        ]),
    html.Div(
        className='app-table',
        children= [
            html.H2('Gas Price Summary By Region'),
            dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in tb.columns],
            data=tb.to_dict('records'),
            style_table={
                'overflowX': 'auto'
            },
            style_as_list_view=True,
            style_cell={
                'height': '70px',
                'width': '85px', 
                'whiteSpace': 'normal',
                'text-align':'center',
                'font-size': '20px ',
                'font-family': 'Arial, Helvetica, sans-serif'
            },
            style_data={
                'color': 'black',
                'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(188, 188, 188)',
                    'color': 'white'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(58, 117, 194)',
                'color': 'black',
                'fontWeight': 'bold',
                'text-align':'center',
                'font-size': '20px',
                'color':'white',
                'font-family': 'Arial, Helvetica, sans-serif'
            }
        )
        ]
    ),
    html.Div(
        className='app-scatter',
        children=[
            dcc.Graph(id = 'Scatter_Plots',className='app-scatter-plot'),
            dcc.Dropdown(
                id = 'my-dropdown',
                className= 'app-scatter-dropdown',
                options = [{'label':i,'value':j} for i ,j in zip(option_labels,option_values)],
                searchable=False,
                value = 'Gas_Tax'),
            html.Hr(),
            dcc.Checklist(
            id = 'my-checklist',
            options = [{'label':'Party Affliation','value': 'party'}],
            labelStyle={'display': 'inline-block',
                        'font-size':'22px',
                        'fontWeight': 'bold',
                        'color':'rgb(58, 117, 194)',
                        'margin-left':'10px'
                        }
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline',
                            'font-size':'22px',
                            'fontWeight': 'bold',
                            'color':'rgb(58, 117, 194)',
                            "padding": "10px"}
            )
        ]
    ),
    html.Div(
        className='app-box',
        children = [
            dcc.Graph(
            className= 'app-box-plot',
            id='box',
            figure=fig1)]
        ),
    html.Div(className='app-time',
        children=[
            dcc.Graph(id='state-line',
                className='app-time-plot',
                 figure={
                    'layout': {'margin': {'l': 0, 'b': 0, 't': 0, 'r': 0}}
                }
            ),
            html.P('Please select the region you are interested in',
                style = {
                    'fontSize': '25px',
                    'text-align': 'right',
                    'margin-top':'10px',
                    'fontWeight': 'bold',
                    'color':'rgb(58, 117, 194)'
                }),
            dcc.Dropdown(
                id='line_state_dropdown',
                className='app-time-drop',
                options=[{'label': i, 'value': i} for i in price.columns],
                value='East Coast',
                style = {
                    'width': '50vh',
                    'float':'right'
                })
        ], style={
            'width': '90%', 
            'display': 'inline-block',
            'padding': '10 5',
            'margin':'narrow' 
            }),
    html.Div(
        className= 'app-footer',
        children= [
            html.Hr(className='hr'),
            html.H6('DSO545 Final Project (Fall 2021) - Zihang Li, Freda Lin, Zihan Ling, Jingchen Liu, Yafan Zeng, Pizheng Zhang')
        ]
        )
])

@app.callback(
    [Output('Scatter_Plots', 'figure'),
    Output('statemap', 'figure'),
    Output('state-line', 'figure')],
    [Input('my-dropdown', 'value'),
    Input('my-checklist', 'value'),
    Input('xaxis-type', 'value'),
    Input('map_state_dropdown', 'value'),
    Input('line_state_dropdown', 'value')]
)
def update_output(x_value,par,mode,state,padd):
    ############### Scatter ##################
    m = None
    if x_value is None:
        x_value == 'Gas Tax'
    if mode == 'Log':
        m = True
    p = None
    if par:
        p = 'Party'
    fig1 = px.scatter(data_frame=final,x=x_value,y='Gas_Price', color = p,
                     color_discrete_map = {'Democrat':'blue','Republic':'red'},
                     labels= {'Gas_Price':'Price ($)',
                             x_value: xaxis_labels[x_value]},
                     text = 'ST',
           hover_data=['State','Gas_Price', 'Auto', 'Population'],
           trendline="ols",log_x=m)

    fig1.update_traces(textposition = 'bottom right',marker = dict(size = 8))
    fig1.update_layout(legend_traceorder="reversed",
                        title={
                            'text': f'Avg. Retail Gas Price vs. {title_labels[x_value]} By State',
                            'font_size': 25,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'
                            },
                        plot_bgcolor='white',
                        xaxis=dict(
                            showline=True,
                            showticklabels=True,
                            linecolor='rgb(204, 204, 204)',
                            linewidth=2,
                            ticks='outside',
                            tickfont=dict(
                                family='Arial',
                                size=12,
                                color='rgb(82, 82, 82)',
                                )
                            ),
                        yaxis=dict(
                                showline=True,
                                showticklabels=True,
                                showgrid=True,
                                gridcolor='rgb(204, 204, 204)'
                            )
                        )
    ############### Map ##################
    if state is None:
        df2 = df_map[df_map['state']=='CA']
    else:
        df2 = df_map[df_map['state']==state]
    # fig2 = figure(figsize = (10, 6), dpi = 80)
    fig2 = px.choropleth(df2, 
                        geojson=counties, 
                        locations='FIPS', 
                        color='price',
                        color_continuous_scale="jet",
                        hover_name="county",
                        range_color=(df_map['price'].min()-0.1, df_map['price'].max()+0.1)
                        )
    fig2.update_geos(fitbounds='locations', visible=False)
    fig2.update_traces(marker_line_width=0.3)
    fig2.update_layout(title={
                            'text': 'gas price by county in State ' + state,
                            'font_size': 25,
                            'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'
                            })
    fig2.update_layout(margin={"r":1,"l":2,"b":0})
    ############### Line ##################
    if padd is None:
        padd = 'East Coast'

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(
        go.Scatter(x=price.index, y=price[padd],name="Gas Price", marker_color='red'),
        secondary_y=False
    )
    fig3.add_trace(
        go.Scatter(x=production.index, y=production[padd],name='Crude Oil Production', marker_color='green'),
        secondary_y=True
    )
    fig3.update_xaxes(rangeslider_visible = True)
    fig3.update_yaxes(title_text="Gas Price", secondary_y=False)
    fig3.update_yaxes(title_text='Crude Oil Production', secondary_y=True)
    fig3.update_layout(
        title={
            'text': padd + ' Yearly Average Gas Price VS Crude Oil Production',
            'font_size': 30,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor='white',
        legend=dict(
            font_size=12,
            x=0.1, y=1,
            yanchor='top',
            xanchor='center',
            bgcolor = 'white', 
            borderwidth = 0.5
        ),
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(0, 0, 0)',
            linewidth=1,
            ticks='outside'
       ),
       yaxis1=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(0, 0, 0)',
            linewidth=1,
            ticks='outside'
       ),
       yaxis2=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(0, 0, 0)',
            linewidth=1,
            ticks='outside'
       ),  
    )

    return fig1, fig2, fig3

if __name__ == '__main__':
    app.run_server(debug=True)









