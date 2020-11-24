# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Importing Libraries

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from time import time
import datetime as dt
import calendar

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/superhero/bootstrap.min.css', "https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css", 'styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

df_labels = pd.read_excel("../data/Analysis/Meter Names and Labels.xlsx")

names_cleaned = []

for item in df_labels["Name"]:
    name = item.split("-")[0].replace("'", "").replace(" ", "").strip()
    if name == "JacksonLibraryTower_kWh":
        name = "JacksonLibraryTower"
    names_cleaned.append(name)

df_labels["Names_cleaned"] = names_cleaned

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#ffb71b",
    "color": "#0f2044"
}

# the styles for the main content position it is to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "backgroundColor": "#0f2044",
    "fontFamily": "Sofia Pro"
}

NAVLINK = {
    "color": "#0f2044"
}

NAVLINK_ACTIVE = {
    "color": "#fff",
    "backgroundColor": "#0f2044"
}

LAYOUT = {
    "backgroundColor": "#0f2044",
    "fontFamily": "Sofia Pro",
    "height": "100vh"
}

DROPDOWN = {
    "color": "black"
}

LABEL = {
    "height": "25px"
}

HEADER = {
    "fontWeight": "bold",
}

SUBTITLE = {
    "color": "#fff",
    "fontWeight": "bold"
}

CONTENT_HEADER = {
    "paddingTop": "1rem",
    "color": "#ffb71b",
    "fontSize": "x-large"
}

HELP = {
    "fontSize": "x-large",
}

HELP_BUTTON = {
    "margin": "1rem",
    "backgroundColor":"#0f2044"
}

MODAL = {
    "backgroundColor":"#fff"
}

# Sidebar Layout
sidebar = html.Div(
    [
        html.H4("Hackathon", className="display-6", style=HEADER),
        html.Hr(),
        html.P(
            "Funded by the UNCG Green Fund", className="lead", style=SUBTITLE
        ),
        dbc.Nav(
            [
                dbc.NavLink("Energy Consumption & Prediction", href="/task-1", id="page-1-link", style=NAVLINK, className="navlink-active"),
                dbc.NavLink("Average Predictions By Group", href="/task-2", id="page-2-link", style=NAVLINK, className="navlink-active"),
            ],
            vertical=True,
            pills=True
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

# Layout for Task-1
content_T1_layout = html.Div([
    dbc.Container([
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Span([
                            html.Span("Energy Consumption & Prediction", style=CONTENT_HEADER),
                            html.Span([
                                html.A(html.I(className="fa fa-question-circle", style=HELP), id="open", style=HELP_BUTTON, title="Help"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Help"),
                                        dbc.ModalBody([
                                            html.H5("Energy consumption- Actual and Predicted"),
                                            html.Div([
                                                html.P("User should select a meter or multiple meters for which they want to visualise the graph"),
                                                html.Div([
                                                    html.P("Then select a time interval which has the options Hour, Week, Month, Day and Time."),
                                                    html.P("1. Hour: Please select to and from dates and to and from hours(Note: Select dates which are less then 6 months to check the hourly consumption otherwise it may take a longer time to load)."),
                                                    html.P("2. Week: Once you click on week you will get Year and Week dropdown and you can select both the options and you can see the consumption graph for the weeks of the selected year."),
                                                    html.P("3. Month: Once you select the dates from the datepicker, you will get all the months consumption for that specific period of time."),
                                                    html.P("4. Year: Once you select the dates from the datepicker, you will get the years consumption for the selected period of time."),
                                                    html.P("5. Day: Once you select the to and from dates from the datepicker you will get the daily consumption of all the dates between the selected dates."),
                                                ], className="HelpSubText"),
                                                html.P("User can choose from average and total consumption for all the above graphs from the dropdown."),
                                                html.P("We have a Predictions checkbox if you click that user will get the actual and predicted graph for all the above conditions. And for the hourly consumption we have the displayed prediction interval too."),
                                                html.P("We also have a range slider for all the graphs where the user can shrink to to see detailed data.")

                                            ], className="HelpText"),
                                            


                                        ]
                                        ),
                                        dbc.ModalFooter(
                                            dbc.Button("Close", id="close", className="ml-auto")
                                        ),
                                    ],
                                    id="modal",
                                    size="xl",
                                    className= "mymodel"
                                )
                                ])])
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.P("Meters :"),
                    style=LABEL
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="meters",
                        options=[{"label": row['Label'], "value": row['Names_cleaned']}
                                 for index, row in df_labels.iterrows()],
                        value=[df_labels["Names_cleaned"][0]],
                        clearable=False,
                        multi=True,
                        style=DROPDOWN,
                        className="multi-dropdown-custom"

                    ),

                ),

            ],
            align="start",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.P("Time Interval :"),
                    style=LABEL
                ),

                dbc.Col(
                    html.P("Average/Total Consumption :"),
                    style=LABEL
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(

                    dcc.Dropdown(
                        id="option-dropdown",
                        options=[
                            {'label': 'Year', 'value': 'year'},
                            {'label': 'Month', 'value': 'month'},
                            {'label': 'Week', 'value': 'week'},
                            {'label': 'Day', 'value': 'day'},
                            {'label': 'Hour', 'value': 'hour'},
                        ],
                        value='hour',
                        clearable=False,
                        style=DROPDOWN,
                        className="dropdown-custom"
                    )
                ),
                dbc.Col(

                    dcc.Dropdown(
                        id="demo-dropdown",
                        options=[
                            {'label': 'Total Consumption', 'value': 'TC'},
                            {'label': 'Average Consumption', 'value': 'AC'}
                        ],
                        value='TC',
                        clearable=False,
                        style=DROPDOWN,
                        className="dropdown-custom"
                    )
                )

            ],
            align="start",
        ),
        html.Br(),
        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        html.P("Year :"),
                        style=LABEL
                    ),
                    dbc.Col(
                        html.P("Week :"),
                        style=LABEL
                    )
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {'label': x, 'value': x, 'disabled': False}
                                for x in range(2015, 2022)
                            ],
                            value=['2018', '2019'],
                            multi=True,
                            clearable=True,
                            style=DROPDOWN,
                            className="dropdown-custom"
                        )
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id="week-dropdown",
                            options=[
                                {'label': x, 'value': x, 'disabled': False}
                                for x in range(1, 53)
                            ],
                            value=['30', '35'],
                            multi=True,
                            clearable=True,
                            style=DROPDOWN,
                            className="dropdown-custom"

                        )
                    ),

                ],
                align="start",
            ), ], id='datatable-container'),
        html.Br(),
        html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.P("Date :"),
                    style=LABEL
                ),
                dbc.Col(
                    html.P("Start Time (in hours) :"),
                    style=LABEL
                ),
                dbc.Col(
                    html.P("End Time (in hours) :"),
                    style=LABEL
                ),

            ]
        ),

        dbc.Row(
            [
                dbc.Col(

                    dcc.DatePickerRange(
                        id='my-date-picker-range',
                        min_date_allowed=date(1995, 8, 5),
                        max_date_allowed=date(2021, 11, 12),
                        initial_visible_month=date(2015, 1, 1),
                        start_date=date(2020, 1, 1),
                        end_date=date(2020, 1, 2),
                        className="date-picker-custom"
                    )

                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="start-hour-dropdown",
                        options=[{'label': str(x), 'value': str(x), 'disabled': False}
                                 for x in range(0, 24)],
                        value='0',
                        multi=False,
                        style=DROPDOWN,
                        className="dropdown-custom"
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="end-hour-dropdown",
                        options=[{'label': str(x), 'value': str(x), 'disabled': False}
                                 for x in range(0, 24)],
                        value='23',
                        multi=False,
                        style=DROPDOWN,
                        className="dropdown-custom"
                    )
                )

            ],
            align="start",
        ),],id="datatable-container4"),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(

                    dcc.Checklist(
                        id="prediction-checklist",
                        options=[
                            {'label': 'Predictions', 'value': 'Predictions'}
                        ],
                        value=['Predictions']
                    ),

                ),

            ],
            align="start",
        ),
        html.Div(id='dd-output-container'),
        html.Br(),
        html.Div(
            [   
                dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id="loading-output-2")])],
                    type="circle"
                ),
                dcc.Graph(id='task1_map', figure={})
            ]
        )
    ])
])

# Layout for Task-2
content_T2_layout = html.Div([
    dbc.Container([
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.Span([
                            html.Span("Average Predictions By Group", style=CONTENT_HEADER),
                            html.Span([
                                html.A(html.I(className="fa fa-question-circle", style=HELP), id="open", style=HELP_BUTTON, title="Help"),
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader("Help"),
                                        dbc.ModalBody([
                                            html.H5("Average Predictions By Group"),
                                            html.Div([
                                                html.P("We choose a time category and we get the graph visualised based on that."),
                                                html.P("For example, if the user chooses hour of day, the Bryan Building meter. The graph would plot the average actual and average predicted consumption in Bryan from for the year 2020 by hour of the day. There would be one observation per hour in a day (24 total)."),
                                            ], className="HelpText"),
                                    

                                        ]
                                        ),
                                        dbc.ModalFooter(
                                            dbc.Button("Close", id="close", className="ml-auto")
                                        ),
                                    ],
                                    id="modal",
                                    size="xl",
                                    className= "mymodel"
                                )
                                ])])
                )
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.P("Meters :"),
                    style=LABEL
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="meters_2",
                        options=[{"label": row['Label'], "value": row['Names_cleaned']}
                                 for index, row in df_labels.iterrows()],
                        value=[df_labels["Names_cleaned"][0]],
                        clearable=False,
                        multi=True,
                        style=DROPDOWN,
                        className="multi-dropdown-custom"
                    ),

                ),

            ],
            align="start",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.P("Choose a time category :"),
                    style=LABEL
                ),


            ]
        ),
        dbc.Row(
            [
                dbc.Col(

                    dcc.Dropdown(id='choice_dropdown',
                                 options=[
                                     {'label': 'Hour of Day', 'value': 'hour'},
                                     {'label': 'Day of Week', 'value': 'day'},
                                     {'label': 'Week of Year', 'value': 'week'},
                                     {'label': 'Month of Year', 'value': 'month'},
                                 ],
                                 value='month',
                                 clearable=False,
                                 style=DROPDOWN,
                                 className="dropdown-custom"
                                 ),

                ),


            ],
            align="start",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.P("From Year :"),
                    style=LABEL
                ),
                dbc.Col(
                    html.P(" Month :"),
                    style=LABEL
                ),
                dbc.Col(
                    html.P("To Year :"),
                    style=LABEL
                ),
                dbc.Col(
                    html.P(" Month :"),
                    style=LABEL
                ),

            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                        dcc.Dropdown(
                            id="from-year-dropdown",
                            options=[{'label':'2020', 'value': '2020', 'disabled': False}],
                            value='2020',
                            multi=False,
                            style=DROPDOWN,
                            className="dropdown-custom",
                            clearable=False
                        )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="from-month-dropdown",
                        options=[{'label':calendar.month_name[x] , 'value': str(x), 'disabled': False}
                                 for x in range(1, 12)],
                        value='1',
                        multi=False,
                        style=DROPDOWN,
                        className="dropdown-custom",
                        clearable=False
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="to-year-dropdown",
                        options=[{'label': '2020', 'value': '2020', 'disabled': False}],
                        value='2020',
                        multi=False,
                        style=DROPDOWN,
                        className="dropdown-custom",
                        clearable=False
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="to-month-dropdown",
                        options=[{'label': calendar.month_name[x], 'value': str(x), 'disabled': False}
                                 for x in range(1, 12)],
                        value='7',
                        multi=False,
                        style=DROPDOWN,
                        className="dropdown-custom",
                        clearable=False
                    )
                ),

            ],
            align="start",
        ),
        html.Br(),
        html.Div(id='dummy-container'),
        dcc.Graph(id='task2_map', figure={})
    ])
])

# App Layout
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
], style=LAYOUT)


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 3)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/task-{i}" for i in range(1, 3)]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/task-1"]:
        return content_T1_layout
    elif pathname == "/task-2":
        return content_T2_layout
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Callback for Task-1
@app.callback(
    dash.dependencies.Output('datatable-container', 'style'),
    [dash.dependencies.Input('option-dropdown', 'value')])
def toggle_container3(toggle_value):
    if toggle_value == 'week':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    dash.dependencies.Output('datatable-container4', 'style'),
    [dash.dependencies.Input('option-dropdown', 'value')])
def toggle_container1(toggle_value):
    if toggle_value == 'year' or toggle_value == 'month' or toggle_value == 'day' or toggle_value == 'hour':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    [dash.dependencies.Output("loading-output-2", "figure"),
     dash.dependencies.Output('dd-output-container', 'string_prefix'),
     dash.dependencies.Output('task1_map', 'figure')],
    [dash.dependencies.Input('meters', 'value'),
     dash.dependencies.Input('option-dropdown', 'value'),
     dash.dependencies.Input('demo-dropdown', 'value'),
     dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date'),
     dash.dependencies.Input('start-hour-dropdown', 'value'),
     dash.dependencies.Input('end-hour-dropdown', 'value'),
     dash.dependencies.Input('prediction-checklist', 'value'),
     dash.dependencies.Input('year-dropdown', 'value'),
     dash.dependencies.Input('week-dropdown', 'value')
     ])
def update_output(meters, selected_value, value, start_date, end_date, start_hour, end_hour, pred_, year, week):
    start_time = time()
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        mytime = dt.datetime.strptime(start_hour, '%H').time()
        start_datetime_object = dt.datetime.combine(start_date_object, mytime)
        start_date_string = start_datetime_object.strftime('%B %d, %Y  %H:%M')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        mytime = dt.datetime.strptime(end_hour, '%H').time()
        end_datetime_object = dt.datetime.combine(end_date_object, mytime)
        end_date_string = end_datetime_object.strftime('%B %d, %Y %H:%M')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        string_prefix = 'Select a date to see it displayed here'

    def f(df):
        # df = df.copy()
        # df['Datetime'] = df['Datetime']
        df['Date'] = df['Datetime'].dt.strftime('%Y-%m-%d')
        df['Year'] = df['Datetime'].dt.year
        df['Month'] = df['Datetime'].dt.strftime('%Y-%m')
        df['Week'] = df['Datetime'].dt.week
        df['Day'] = df['Datetime'].dt.strftime('%Y-%m-%d')
        df['Hour'] = df['Datetime'].dt.strftime('%Y-%m-%d %H')
        df['Year-Week'] = df['Datetime'].dt.week.astype(str) + '-' +  df['Datetime'].dt.year.astype(str) 
        return df

    layout = go.Layout(
        autosize=False,
        height=350,

        xaxis=go.layout.XAxis(linecolor='black',
                              linewidth=1,
                              mirror=True),

        yaxis=go.layout.YAxis(linecolor='black',
                              linewidth=1,
                              mirror=True)

    )

    fig = go.Figure(layout=layout)

    for meter in meters:

        df_meter = pd.read_csv("../data/Analysis/" + meter + "_results.csv")
        df_meter['Datetime'] = pd.to_datetime(df_meter['Datetime'], utc=True)
        df_week_meter = pd.read_csv("../data/Analysis/" + meter + "_results.csv")
        df_week_meter['Datetime'] = pd.to_datetime(df_meter['Datetime'], utc=True)
        df_meter = df_meter[(df_meter['Datetime'] >= pd.to_datetime(start_datetime_object, utc=True)) &
                            (df_meter['Datetime'] <= pd.to_datetime(end_datetime_object, utc=True))]
        
        df_meter = f(df_meter)
        df_week_meter = f(df_week_meter)

        # df_meter['Date'] = df_meter.Datetime.apply(lambda d: d.split(" ", 1)[0])
        if value == 'TC':
            y_label = "Total Energy Consumption"
            if selected_value == 'week':
                x_label = "Week"
                fig_title = "Total Energy Consumption for each week"
                df_selected = df_week_meter[df_week_meter['Year'].isin(year)]
                df_selected = df_selected[df_selected['Week'].isin(week)]
                df_selected = df_selected.groupby("Year-Week").agg(
                    {'Hour': 'count', 'Actual': 'sum', 'Predicted': 'sum'}).reset_index()
                x = df_selected["Year-Week"]
            elif selected_value == 'day':
                x_label = "Day"
                fig_title = "Total Energy Consumption for each day"
                df_selected = df_meter.groupby(["Date"]).sum().reset_index()
                x = df_selected["Date"]
            elif selected_value == 'hour':
                x_label = "Hour"
                fig_title = "Total Energy Consumption for each hour"
                df_selected = df_meter
                x = df_selected["Hour"]
            elif selected_value == 'month':
                x_label = "Month"
                fig_title = "Total Energy Consumption for each month"
                df_selected = df_meter.groupby(["Month"]).sum().reset_index()
                x = df_selected["Month"]
            else:
                x_label = "Year"
                fig_title = "Total Energy Consumption for each year"
                df_selected = df_meter.groupby(["Year"]).sum().reset_index()
                x = df_selected["Year"]
        else:
            y_label = "Average Hourly Energy Consumption"
            if selected_value == 'week':
                x_label = "Week"
                fig_title = "Average Hourly Energy Consumption by week"
                df_selected = df_week_meter[df_week_meter['Year'].isin(year)]
                df_selected = df_selected[df_selected['Week'].isin(week)]
                df_selected = df_selected.groupby("Year-Week").agg(
                    {'Hour': 'count', 'Actual': 'mean', 'Predicted': 'mean'}).reset_index()
                x = df_selected["Year-Week"]
            elif selected_value == 'day':
                x_label = "Day"
                fig_title = "Average Hourly Energy Consumption by day"
                df_selected = df_meter.groupby(["Date"]).mean().reset_index()
                x = df_selected["Date"]
            elif selected_value == 'hour':
                x_label = "Hour"
                fig_title = "Average Hourly Energy Consumption by hour"
                df_selected = df_meter
                x = df_selected["Hour"]
            elif selected_value == 'month':
                x_label = "Month"
                fig_title = "Average Hourly Energy Consumption by month"
                df_selected = df_meter.groupby(["Month"]).mean().reset_index()
                x = df_selected["Month"]
            else:
                x_label = "Year"
                fig_title = "Average Hourly Energy Consumption by year"
                df_selected = df_meter.groupby(["Year"]).mean().reset_index()
                x = df_selected["Year"]

        if len(pred_) != 0:
            fig.add_trace(go.Scatter(
                name=meter + ' Actual',
                mode='markers', x=x, y=df_selected["Actual"]
            ))

            fig.add_trace(go.Scatter(
                name=meter + ' Predicted',
                mode="markers+lines", x=x, y=df_selected["Predicted"]
            ))

            if selected_value == 'hour':
                fig.add_trace(go.Scatter(
                    name=meter + ' Lower',
                    mode="lines", x=x, y=df_selected["obs_ci_lower"],
                    fill="tonexty",
                    marker={"color": "rgba(135, 206, 250, 0.1)"},
                ))

                fig.add_trace(go.Scatter(
                    name=meter + ' Upper',
                    mode="lines", x=x, y=df_selected["obs_ci_upper"],
                    fill="tonexty",
                    marker={"color": "rgba(135, 206, 250, 0.1)"},
                ))

        else:
            fig.add_trace(go.Scatter(
                name=meter,
                mode="markers+lines", x=x, y=df_selected["Actual"]
            ))

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    string_prefix = string_prefix + "; response time is {:04f} seconds".format(time() - start_time)

    fig.update_layout(title=fig_title, xaxis_title=x_label, yaxis_title=y_label, legend_title="Meters",)

    return fig, string_prefix, fig


@app.callback(
    [dash.dependencies.Output('task2_map', 'figure')],
    [dash.dependencies.Input('meters_2', 'value'),
     dash.dependencies.Input('choice_dropdown', 'value'),
     dash.dependencies.Input('from-year-dropdown', 'value'),
     dash.dependencies.Input('from-month-dropdown', 'value'),
     dash.dependencies.Input('to-year-dropdown', 'value'),
     dash.dependencies.Input('to-month-dropdown', 'value')])
def update_output_2(meters, category_value, start_year, start_month, end_year, end_month):

    start_date_object = dt.datetime.strptime(start_year+start_month, "%Y%m").date()
    end_date_object = dt.datetime.strptime(end_year + end_month + str(calendar.monthrange(int(end_year), int(end_month))[1]), "%Y%m%d").date()

    def f(df):
        # df = df.copy()
        # df['Datetime'] = df['Datetime']
        df['Month'] = df['Datetime'].dt.month
        df['Weekday'] = df['Datetime'].apply(lambda t: t.weekday())
        df['Week'] = df['Datetime'].dt.week
        df['Day'] = df['Datetime'].dt.day
        df['Hour'] = df['Datetime'].dt.hour
        df['Year-Week'] = df['Datetime'].dt.year.astype(str) + '-' + df['Datetime'].dt.week.astype(str)
        return df

    layout = go.Layout(
            autosize=False,
            height=500,

            xaxis=go.layout.XAxis(linecolor='black',
                                  linewidth=1,
                                  mirror=True,),

            yaxis=go.layout.YAxis(linecolor='black',
                                  linewidth=1,
                                  mirror=True),
        )

    fig = go.Figure(layout=layout)

    for meter in meters:

        df_meter = pd.read_csv("../data/Analysis/" + meter + "_results.csv")
        df_meter['Datetime'] = pd.to_datetime(df_meter['Datetime'], utc=True)
        df_meter = df_meter[(df_meter['Datetime'] >= pd.to_datetime(start_date_object, utc=True)) &
                            (df_meter['Datetime'] <= pd.to_datetime(end_date_object, utc=True))]
        df_meter = f(df_meter)

        # df_meter['Date'] = df_meter.Datetime.apply(lambda d: d.split(" ", 1)[0])
        if category_value == 'month':
            df_selected = df_meter.groupby("Month").mean().reset_index()
            x = df_selected["Month"]
            fig_title = "Usage on basis of Month of the Year"
            x_title = "Month"
        if category_value == 'day':
            fig_title = "Usage on basis of Day of the Week"
            df_selected = df_meter.groupby("Weekday").mean().reset_index()
            x = df_selected["Weekday"]
            x_title = "Day"
        elif category_value == 'hour':
            fig_title = "Usage on basis of Hour of the Day"
            df_selected = df_meter.groupby(["Hour"]).mean().reset_index()
            x = df_selected["Hour"]
            x_title = "Hour"
        elif category_value == 'week':
            fig_title = "Usage on basis of Week of the Year"
            df_selected = df_meter.groupby(["Week"]).mean().reset_index()
            x = df_selected["Week"]
            x_title = "Week"

        fig.add_trace(go.Scatter(
            name=meter + ' Actual',
            mode='markers', x=x, y=df_selected["Actual"]
        ))

        fig.add_trace(go.Scatter(
            name=meter + ' Predicted',
            mode="markers+lines", x=x, y=df_selected["Predicted"]
        ))



    fig.update_xaxes(
        title_text = x_title,
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        dtick = 1
    )
    fig.update_yaxes(title_text = "Usage in Units")
    if category_value == "month":
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            )
        )
    elif category_value =="day":
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6],
                ticktext=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            )
        )
    elif category_value =="hour":
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
                ticktext=['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM',
                          '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM']
            )
        )

    fig.update_layout(title=fig_title, legend_title="Meters")

    return [fig]


if __name__ == '__main__':
    app.run_server(debug=True)