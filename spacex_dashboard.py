# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print(spacex_df.head())
# Create a dash application
app = dash.Dash(__name__)
print(spacex_df['Launch Site'].unique())
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    ],
                                    value='ALL',
                                    placeholder="",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i:str(i) for i in range(0,10001,2500)},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    #filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Total successful Launches by Site')
        return fig
    else:
        df = spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df = df.groupby(['class']).size().reset_index(name='counts')
        filtered_df['percentage'] = 100 * filtered_df['counts'] / filtered_df['counts'].sum()

        fig = px.pie(filtered_df, values='percentage', 
            names='class', 
            title=f'Successful launch percentage for site {entered_site}')
        
        return fig
        # return the outcomes piechart for a selected site
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site,entered_payload):
    print(entered_payload)
    df = spacex_df[np.logical_and(np.greater_equal(spacex_df['Payload Mass (kg)'].values,entered_payload[0]),np.less_equal(spacex_df['Payload Mass (kg)'].values,entered_payload[1]))]
    if entered_site == 'ALL':
        fig = px.scatter(df,x='Payload Mass (kg)',y='class',title='Payload Mass (kg) vs Success of Launch',
            color='Booster Version Category')
    else:
        df = df[spacex_df['Launch Site']==entered_site]
        fig = px.scatter(df,x='Payload Mass (kg)',y='class',title='Payload Mass (kg) vs Success of Launch',
            color='Booster Version Category')
    
    return fig
    
# Run the app
if __name__ == '__main__':
    app.run_server()
