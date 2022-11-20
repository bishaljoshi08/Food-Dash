from dash import Dash, html, dcc, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import time



# # df_interactions = pd.read_csv("datasets/RAW_interactions.csv")
df_recepies = pd.read_csv("datasets/Transformed_recipes.csv")
df_ingredient = pd.read_csv('datasets/ingredients_count.csv')
print(df_recepies.duplicated().sum())
df = df_recepies[['n_steps','n_ingredients','Calories','TotalFat','Sugar','Sodium','Protein','SaturatedFat','Carbohydrates','name','minutes']]
df_recepies_sample = df_recepies.sample(n=10)
counts_label = {'Step Count': 'n_steps', 'Ingredients count':'n_ingredients','Calories': 'Calories', 'Total Fat': 'TotalFat', 'Sugar': 'Sugar', 'Sodium': 'Sodium', 'Protein': 'Protein', 'Saturated Fat': 'SaturatedFat', 'Carbohydrates': 'Carbohydrates','Minutes':'minutes'}
nutrition_fact = {'Calories': 'Calories', 'Total Fat': 'TotalFat', 'Sugar': 'Sugar', 'Sodium': 'Sodium', 'Protein': 'Protein', 'Saturated Fat': 'SaturatedFat', 'Carbohydrates': 'Carbohydrates'}
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = 'Food dashboard'
sidebar = dbc.Card([
    dbc.CardBody([
        html.H2('Food Dash', className='display-4'),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink('Home', href='/', active='exact'),
                dbc.NavLink('Scatter Plot', href='/scatterplot', active='exact'),
                dbc.NavLink('Table', href='/table', active='exact'),
                dbc.NavLink('Most Used Ingredients', href='/barchart', active='exact'),
            ],
            vertical=True,
            pills=True,
            
        )
    ])
],
color='light', style={'height': '100vh', 'width':'16rem', 'position':'fixed'
})

content = html.Div(id='seperate-page', style = {'padding': '3rem'})

app.layout = dbc.Container([
    dcc.Location(id='url'),
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(content, width=9, style={'margin-left': '16rem'})
    ])
], fluid=True)
@app.callback(
    Output(component_id='scatterplot_with_x_y', component_property='figure'),
    Input(component_id='value_dropdown_x', component_property='value'),
    Input(component_id= 'value_dropdown_y', component_property='value'),
    Input(component_id= 'value_dropdown_color', component_property='value'),
    Input(component_id= 'value_dropdown_size', component_property='value'),
)
def update_scatterplot(x,y,color,size):
    fig = px.scatter(data_frame=df_recepies, x=x, y=y, color=color, size=size)
    fig.update_layout(transition_duration = 500)
    return fig



@app.callback(
    Output("detail", "children"),
    [Input("value_dropdown_choose", "value")]
)
def update_home(value):
            

    mask = df_recepies_sample['name'] == value
    # for each in df_recepies_sample[mask]:
    #     print(each.values())    
    print(df_recepies_sample[mask]['name'])
    return html.Div([
        html.Br(),
        dbc.ListGroup([
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Name: '), width=2), dbc.Col(html.P(f'{value}'),width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Ingredients count: '), width=2), dbc.Col(html.P('{}'.format(df_recepies_sample[mask]['n_ingredients'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Step count: '), width=2), dbc.Col(html.P('{}'.format(df_recepies_sample[mask]['n_steps'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Time to prepare '), width=2), dbc.Col(html.P('{} min'.format(df_recepies_sample[mask]['minutes'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Ingredients: '), width=2), dbc.Col(html.P('{}'.format(df_recepies_sample[mask]['ingredients'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Steps: '), width=2), dbc.Col(html.P('{}'.format(df_recepies_sample[mask]['steps'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Description: '), width=2), dbc.Col(html.P('{}'.format(df_recepies_sample[mask]['description'].iloc[0])), width=10)] )),

                    ]),
        html.Br(),
        
        dbc.ListGroup([
                        dbc.ListGroupItem(dbc.Col(html.H5('Nutrition Fact'), width=2)),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Calories: '), width=2), dbc.Col(html.P('{} cal'.format(df_recepies_sample[mask]['Calories'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Protein: '), width=2), dbc.Col(html.P('{} PDV'.format(df_recepies_sample[mask]['Protein'].iloc[0])), width=10)] )), 

                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Carbohydrates: '), width=2), dbc.Col(html.P('{} PDV'.format(df_recepies_sample[mask]['Carbohydrates'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Total Fat: '), width=2), dbc.Col(html.P('{} PDV'.format(df_recepies_sample[mask]['TotalFat'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Saturated Fat: '), width=2), dbc.Col(html.P('{} PDV'.format(df_recepies_sample[mask]['SaturatedFat'].iloc[0])), width=10)] )),
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Sugar: '), width=2), dbc.Col(html.P('{} PDV'.format(df_recepies_sample[mask]['Sugar'].iloc[0])), width=10)] )), 
                        dbc.ListGroupItem(dbc.Row([dbc.Col(html.H6('Sodium: '), width=2), dbc.Col(html.P('{} PDV'.format(df_recepies_sample[mask]['Sodium'].iloc[0])), width=10)] )), 
                        
                    ]),

        
        
    ])
@app.callback(
    Output("seperate-page", "children"),
    [Input("url", "pathname")]
)




def render_page_content(pathname):
    if pathname == "/":
        return [
                html.H1('Know the Data',style={'textAlign':'center'}),
                html.Br(),
                dbc.Col([
                    dbc.Row(
                        html.P('Detailed discription of the given food is as follow:'), style={'justify-content': 'center'}
                    ),
                    dbc.Row(
                        dcc.Dropdown(
                            id="value_dropdown_choose",
                            options=[{"label": value, "value": value} for value in  df_recepies_sample['name']],
                            value=df_recepies_sample['name'].iat[0],
                        ), style={'justify-content': 'center'}
                    ),
                    dbc.Card( id= 'detail')
                ])
               
                
                ]
    elif pathname == "/scatterplot":
        
        return [
                dbc.Container([html.H1('Scatter Plot',  style={'textAlign':'center'}),
    
                dcc.Graph(id="scatterplot_with_x_y"),
                html.Div([
                    html.Div([
                    html.H6("X-axis"),
                    dcc.Dropdown(
                        id="value_dropdown_x",
                        options=[{"label": label, "value": value} for label, value in  counts_label.items()],
                        value=list(counts_label.values())[3],
                    ),
                    ],style={'width': '24%', 'display': 'inline-block'}),
                    html.Div([
                        html.H6("Y-axis"),
                        dcc.Dropdown(
                            id="value_dropdown_y",
                            options=[{"label": label, "value": value} for label, value in  counts_label.items()],
                            value=list(counts_label.values())[2],
                        ),
                    ]
                    ,style={'width': '24%', 'display': 'inline-block'}),
                    html.Div([
                        html.H6("Color"),
                        dcc.Dropdown(
                            id="value_dropdown_color",
                            options=[{"label": label, "value": value} for label, value in  counts_label.items()],
                            value=list(counts_label.values())[7],

                        ),       
                    ]
                    ,style={'width': '24%', 'display': 'inline-block'}),
                    html.Div([
                        html.H6("Size"),
                        dcc.Dropdown(
                            id="value_dropdown_size",
                            options=[{"label": label, "value": value} for label, value in  counts_label.items()],
                            value=list(counts_label.values())[8],
                        ),
                    ]
                    ,style={'width': '24%', 'display': 'inline-block'}),
                ], style={'display': 'flex', 'justify-content': 'space-between'}),
                ])
            ]
    elif pathname == "/table":
        table_columns  = [
            {'name': 'Food Name', 'id': 'name', 'type': 'text', 'sortable': False},
            {'name': 'Step Count', 'id': 'n_steps', 'type': 'numeric', 'sortable': True},
            {'name': 'Item Count', 'id': 'n_ingredients', 'type': 'numeric', 'sortable': True},
            {'name': 'Time(in mins)', 'id': 'minutes', 'type': 'numeric', 'sortable': True},
            {'name': 'Calories', 'id': 'Calories', 'type': 'numeric', 'sortable': True},
            {'name': 'Total Fat(%DV)', 'id': 'TotalFat', 'type': 'numeric', 'sortable': True},
            {'name': 'Sugar(%DV)', 'id': 'Sugar', 'type': 'numeric', 'sortable': True},
            {'name': 'Sodium(%DV)', 'id': 'Sodium', 'type': 'numeric', 'sortable': True},
            {'name': 'Protein(%DV)', 'id': 'Protein', 'type': 'numeric', 'sortable': True},
            {'name': 'Sat. Fat(%DV)', 'id': 'SaturatedFat', 'type': 'numeric', 'sortable': True},
            {'name': 'Carbs(%DV)', 'id': 'Carbohydrates', 'type': 'numeric', 'sortable': True},
        ]
        non_sortable_column_ids = [col['id'] for col in table_columns if col.pop('sortable') is False]
        table_css = [
            {
                'selector': f'th[data-dash-column="{col}"] span.column-header--sort',
                'rule': 'display: none',
            }
            for col in non_sortable_column_ids
        ]
        return [
                html.H1('Table',  style={'textAlign':'center'}),
                my_table := dash_table.DataTable(
                    columns=table_columns,
                    css=table_css,
                    data=df.to_dict('records'),
                    page_size=10,
                    sort_action='native',
                    style_data={
                        'minWidth': '75px', 'maxWidth': '200px','textOverflow': 'ellipsis'
                    
                    }
                ),
                ]
    elif pathname == '/barchart':
        # df_ingredient.loc[df_ingredient['count'], 'ingredient' ] = 'Others'
        fig = px.bar(df_ingredient.head(10), y='count', x= 'ingredient', title = 'Top 10 most used ingredients')

        return [
            dcc.Graph(figure=fig),
        ]

if __name__ == '__main__':
    app.run_server(debug=True)