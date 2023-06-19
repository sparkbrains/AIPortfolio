# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
from dash import dash_table
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_mantine_components as dmc
import plotly.express as px
import os

df = pd.read_csv('/home/spark/Desktop/project/python10/AIPortfolio/datascience_portfolio/ML_Models/dashboard/Employee-Attrition.csv')
Under_25 = df[df['Age'] < 25]
Age_25 = df[(df['Age'] >= 25) & (df['Age'] < 35)]
Age_35 = df[(df['Age'] >= 35) & (df['Age'] < 45)]
Age_Over_45 = df[df['Age'] >= 45]


# Initialize the app - incorporate a Dash Mantine theme
external_stylesheets = [dmc.theme.DEFAULT_COLORS]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Function for creating a pie chart
def create_pie_chart(df):
    attrition_by_department = df['Attrition'].groupby(df['Department']).value_counts().unstack()
    labels = attrition_by_department.index
    values = attrition_by_department['Yes'].values
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        showlegend=True,  # Set showlegend to True
        legend=dict(  # Customize the legend
            x=1,
            y=0.5,
            bgcolor='black',
            bordercolor='blue',
            borderwidth=2,
            font=dict(color='white')
        ),
        title={
            'text': 'Attrition by Department',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': 'blue', 'size': 20}
        },
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color='blue', width=2)
            )
        ]
    )
    
    # Increase the size of the bounding box
    fig.update_traces(marker=dict(line=dict(width=2)))
    
    return fig

# Function for creating donut chart for attrition by gender
def create_donut_chart(df, dataframe_name):
    filtered_df = df[df['Attrition'] == 'Yes']
    attrition_count = filtered_df['Gender'].value_counts()
    total_attrition = attrition_count.sum()

    fig = go.Figure(data=[go.Pie(labels=attrition_count.index, values=attrition_count.values, hole=0.5)])
    fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=14,
                      marker=dict(colors=['#FFA500', '#008000']))

    fig.update_layout(
        title={
            'text': f"Age {dataframe_name}",
            'x': 0.5,
            'font': {'color': 'blue', 'size': 20}
        },
        annotations=[
            {
                'text': f'{total_attrition}',
                'showarrow': False,
                'x': 0.5,
                'y': 0.5,
                'font': {'color': 'blue', 'size': 14}
            }
        ],
        paper_bgcolor='black',
        plot_bgcolor='black'
    )

    return fig

def create_educationfield_countplot(df):
    fig = px.histogram(df, x='EducationField', color='Attrition')

    # Customize the layout
    fig.update_layout(
        title="Attrition by Education Field",
        xaxis=dict(title="Education Field", tickfont=dict(color='blue')),
        yaxis=dict(title="Count", tickfont=dict(color='blue')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='blue'),
        width=500,  # Increase the width of the graph
        height=400  # Increase the height of the graph
        
    )

    return fig

def create_bar_chart_attrition(df):
    bar_fig = go.Figure(
        go.Bar(
            x=df['Attrition'].value_counts(),
            y=['Employee who stayed', 'Employee who left'],
            orientation='h',
            opacity=0.8
        )
    )

    bar_fig.update_layout(
        title="Count of Attrition",
        xaxis=dict(title="Count", tickfont=dict(color='blue')),
        yaxis=dict(title="Employee Status", tickfont=dict(color='blue')),
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='blue')
    )

    return bar_fig

def create_pie_chart_attrition(df):
    pie_fig = go.Figure(
        go.Pie(
            values=df['Attrition'].value_counts(),
            opacity=0.8
        )
    )

    pie_fig.update_layout(
        title="Distribution of Attrition",
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='blue')
    )

    return pie_fig

# Create the HTML table
grouped_df = df.groupby(['JobRole','JobSatisfaction']).size().reset_index(name='Count')
# Create a dictionary to map the old column names to the new column names
new_column_names = {'JobSatisfaction': 'Job Satisfaction', 'JobRole': 'Job Roles', 'Count': 'Grand Total'}

# Use the rename() function to change the column names
grouped_df = grouped_df.rename(columns=new_column_names)
# Create a pivot table to calculate the counts of each job satisfaction level
pivot_df = grouped_df.pivot_table(values='Grand Total', index='Job Roles', columns='Job Satisfaction', fill_value=0)

# Rename the new columns
pivot_df.columns = ['JobSatisfaction_1', 'JobSatisfaction_2', 'JobSatisfaction_3', 'JobSatisfaction_4']
# Calculate the grand total for each job role
jobroles = ["Healthcare Representative","Human Resources","Laboratory Technician","Manager","Manufacturing Director","Research Director","Research Scientist","Sales Executive","Sales Representative"]
pivot_df = pivot_df.assign(GrandTotal=pivot_df.sum(axis=1))
pivot_df.insert(0,"Job Roles",jobroles)
table = dash_table.DataTable(
    data=pivot_df.to_dict('records'),  # Convert DataFrame to dictionary format
    columns=[{'name': col, 'id': col} for col in pivot_df.columns],
    style_table={
        'overflowX': 'auto',
        'backgroundColor': 'black',  # Set the background color to black
        'width': '100%',
        'minWidth': '100%',
        'maxHeight': '600px',  # Set a maximum height for the table
        'overflowY': 'scroll'  # Enable vertical scrolling
    },
    style_cell={
        'minWidth': '0px',
        'maxWidth': '180px',
        'whiteSpace': 'normal',
        'textAlign': 'left',
        'color': 'blue',  # Set the text color to blue
        'backgroundColor': 'grey'  # Set the background color for cells to grey
    },
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(230, 230, 230)'  # Set background color for odd rows
        },
        {
            'if': {'row_index': 'even'},
            'backgroundColor': 'black',  # Set background color for even rows
            'color': 'white'  # Set the text color for even rows to white
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    },
    editable=True,
    filter_action='native',
    sort_action='native',
    sort_mode='multi',
    row_deletable=True
)

def create_pie_chart_Jobroles(df):
    attrition_by_department = df['Attrition'].groupby(df['JobRole']).value_counts().unstack()
    labels = attrition_by_department.index
    values = attrition_by_department['Yes'].values
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        showlegend=True,
        legend=dict(
            x=1,
            y=0.5,
            bgcolor='black',
            bordercolor='blue',
            borderwidth=2,
            font=dict(color='white')
        ),
        title={
            'text': 'Attrition by Department',
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'color': 'blue', 'size': 20}
        },
        shapes=[]
    )
    
    return fig

   

def create_attrition_plots(df):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Count of Attrition", "Distribution of Attrition"))

    # Add bar chart
    fig.add_trace(
        go.Bar(
            x=df['Attrition'].value_counts(),
            y=['Employee who stayed', 'Employee who left'],
            orientation='h',
            opacity=0.8
        ),
        row=1, col=1
    )

    # Add pie chart
    fig.add_trace(
        go.Pie(
            values=df['Attrition'].value_counts(),
            opacity=0.8
        ),
        row=1, col=2
    )

    fig.update_layout(height=400, showlegend=False)

    return fig

# App layout
app.layout = dmc.Container(
    [
        html.Img(
            src='https://media.licdn.com/dms/image/C4E16AQGzr1cUzjMn5A/profile-displaybackgroundimage-shrink_200_800/0/1627027781772?e=2147483647&v=beta&t=5BKXb2J2q-mgFKynC-MZ6huT5UDIOXTIP0TIeaH44Uk',
            style={'height': '50px', 'margin-right': '10px'}
        ),
        dmc.Title(
            'EMPLOYEE ATTRITION DASHBOARD',
            style={'textAlign': 'center', 'color': 'blue', 'fontSize': '30px', 'margin': '50px auto'},
            color="blue",
            size="h1"
        ),

        dmc.Grid(
            [
                dmc.Col(
                    [
                        dcc.Graph(
                            figure=create_pie_chart(df),
                            id='pie-chart',
                            config={'displayModeBar': False}
                        )
                    ],
                    span=6
                ),
                dmc.Col(
                    [           
                        dcc.RadioItems(
                                        options=[
                                            {'label': 'Age', 'value': 'Age'},
                                            {'label': 'Attrition', 'value': 'Attrition'},
                                            {'label': 'EnvironmentSatisfaction', 'value': 'EnvironmentSatisfaction'},
                                            {'label': 'JobSatisfaction', 'value': 'JobSatisfaction'},
                                            {'label': 'OverTime', 'value': 'OverTime'},
                                            {'label': 'TotalWorkingYears', 'value': 'TotalWorkingYears'}
                                        ],
                                        id='my-dmc-radio-item',
                                        value='Age',
                                        labelStyle={'display': 'inline-block', 'color': 'blue'}
                                    ),
                        dcc.Graph(
                            figure={},
                            id='graph-placeholder',
                            config={'displayModeBar': False}
                        )
                    ],
                    span=6
                ),
            ]
        ),  

        html.Hr(style={'background-color': 'blue', 'height': '3px'}),
        dmc.Grid(
            html.H3('Attrition by Age/Gender', style={'color': 'blue'}),
        ),
        dmc.Grid(
            [   
                dmc.Col(
                    dcc.Graph(
                        figure=create_donut_chart(Under_25, "Under_25"),
                        id='donut-chart1',
                        config={'displayModeBar': False},
                        style={'margin': '3', 'padding': '4'}
                    ),
                    span=3
                ),
                dmc.Col(
                    dcc.Graph(
                        figure=create_donut_chart(Age_25, "25-35"),
                        id='donut-chart2',
                        config={'displayModeBar': False}
                    ),
                    span=3
                ),
                dmc.Col(
                    dcc.Graph(
                        figure=create_donut_chart(Age_35, "35-45"),
                        id='donut-chart3',
                        config={'displayModeBar': False}
                    ),
                    span=3
                ),
                dmc.Col(
                    dcc.Graph(
                        figure=create_donut_chart(Age_Over_45, "Over_45"),
                        id='donut-chart4',
                        config={'displayModeBar': False}
                    ),
                    span=3
                ),
            ]
        ),

        html.Hr(style={'background-color': 'blue', 'height': '3px'}),

        dmc.Grid(
            [
                dmc.Col(
                    children= [
                        html.H3('Job Satisfaction Rating', style={'color': 'blue'}),
                        table
                    ],
                    span=7
                ),
                dmc.Col(
                    children = [
                    dcc.Graph(
                        figure=create_educationfield_countplot(df),
                        id='educationfield',
                        config={'displayModeBar': False}
                    ),
                    ],
                    span=3
                ),
            ],
            style={'column-gap': '20px'},
        ),

         dmc.Grid(
            [
                dmc.Col(
                    children=[
                        dcc.Graph(
                            figure=create_bar_chart_attrition(df),
                            id='bar-chart',
                            config={'displayModeBar': False}
                        )
                    ],
                    span=5
                ),
                dmc.Col(
                    children=[
                        dcc.Graph(
                            figure=create_pie_chart_attrition(df),
                            id='pie-chart-attririon',
                            config={'displayModeBar': False}
                        )
                    ],
                    span=3
                ),
                dmc.Col(
                    [
                        dcc.Graph(
                            figure=create_pie_chart_Jobroles(df),
                            id='pie-chart_jobroles',
                            config={'displayModeBar': False}
                        )
                    ],
                    span=4
                ),
            ]
        ),

    ],
    fluid=True,
    style={'backgroundColor': 'black', 'color': 'blue'}
)

# Callbacks
@app.callback(
    Output('graph-placeholder', 'figure'),
    Input('my-dmc-radio-item', 'value')
)
def update_graph(col_chosen):

    fig = go.Figure(data=[go.Histogram(x=df[col_chosen])])

    fig.update_layout(
    paper_bgcolor='black',
    plot_bgcolor='black',
    xaxis=dict(
        title=col_chosen,
        titlefont=dict(color='white')
    ),
    yaxis=dict(
        title='Count',
        titlefont=dict(color='white')
    ),
    title={
        'text': 'Distribution of {}'.format(col_chosen),
        'x': 0.5,
        'y': 0.95,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'color': 'blue', 'size': 20}
    }
    )

    return fig


# # Run the app
if __name__ == '__main__':
    # pass
    app.run_server(debug=True)