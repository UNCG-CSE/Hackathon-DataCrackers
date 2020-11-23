# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from time import time
import datetime as dt

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/superhero/bootstrap.min.css', 'styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True

df_labels = pd.read_excel("../data/Meter Names and Labels.xlsx")

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
    "padding": "2rem 1rem",
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
    "fontFamily": "Sofia Pro"
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
                dbc.NavLink("Task 1", href="/task-1", id="page-1-link", style=NAVLINK, className="navlink-active"),
                dbc.NavLink("Task 2", href="/task-2", id="page-2-link", style=NAVLINK, className="navlink-active"),
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
                        style=DROPDOWN
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
                        value='year',
                        clearable=False,
                        style=DROPDOWN
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
                        style=DROPDOWN
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
                            style=DROPDOWN
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
                            style=DROPDOWN

                        )
                    ),

                ],
                align="start",
            ), ], id='datatable-container'),
        html.Br(),
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
                        initial_visible_month=date(2017, 8, 5),
                        start_date=date(2015, 1, 1),
                        end_date=date(2020, 11, 12)
                    )

                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="start-hour-dropdown",
                        options=[{'label': str(x), 'value': str(x), 'disabled': False}
                                 for x in range(0, 24)],
                        value='0',
                        multi=False,
                        style=DROPDOWN
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="end-hour-dropdown",
                        options=[{'label': str(x), 'value': str(x), 'disabled': False}
                                 for x in range(0, 24)],
                        value='23',
                        multi=False,
                        style=DROPDOWN
                    )
                )

            ],
            align="start",
        ),
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
        dcc.Graph(id='task1_map', figure={})
    ])
])

# Layout for Task-2
content_T2_layout = html.Div([
    dbc.Container([
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
                        style=DROPDOWN
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
                        id="option-dropdown-2",
                        options=[
                            {'label': 'Year', 'value': 'year'},
                            {'label': 'Month', 'value': 'month'},
                            {'label': 'Week', 'value': 'week'},
                            {'label': 'Day', 'value': 'day'},
                            {'label': 'Hour', 'value': 'hour'},
                        ],
                        value='year',
                        clearable=False,
                        style=DROPDOWN
                    )
                ),

                dbc.Col(

                    dcc.Dropdown(
                        id="demo-dropdown-2",
                        options=[
                            {'label': 'Total Consumption', 'value': 'TC'},
                            {'label': 'Average Consumption', 'value': 'AC'}
                        ],
                        value='TC',
                        clearable=False,
                        style=DROPDOWN
                    )
                )

            ],
            align="start",
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    html.P("Date :"),
                    style=LABEL
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(

                    dcc.DatePickerRange(
                        id='my-date-picker-range-2',
                        min_date_allowed=date(1995, 8, 5),
                        max_date_allowed=date(2021, 11, 12),
                        initial_visible_month=date(2017, 8, 5),
                        start_date=date(2015, 1, 1),
                        end_date=date(2020, 11, 12)
                    )

                ),

            ],
            align="start",
        ),
        html.Br(),
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
    [dash.dependencies.Output('dd-output-container', 'string_prefix'),
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

    layout = go.Layout(
        autosize=False,
        height=400,

        xaxis=go.layout.XAxis(linecolor='black',
                              linewidth=1,
                              mirror=True),

        yaxis=go.layout.YAxis(linecolor='black',
                              linewidth=1,
                              mirror=True),

        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=20,
            pad=4
        )
    )

    def f(df):
        # df = df.copy()
        # df['Datetime'] = df['Datetime']
        df['Date'] = df['Datetime'].dt.strftime('%B %d, %Y')
        df['Year'] = df['Datetime'].dt.year
        df['Month'] = df['Datetime'].dt.month
        df['Week'] = df['Datetime'].dt.week
        df['Day'] = df['Datetime'].dt.day
        df['Hour'] = df['Datetime'].dt.strftime('%Y-%m-%d %H')
        df['Year-Week'] = df['Datetime'].dt.year.astype(str) + '-' + df['Datetime'].dt.week.astype(str)
        return df

    fig = go.Figure(layout=layout)

    for meter in meters:

        df_meter = pd.read_csv("../data/" + meter + "_results.csv")
        df_meter['Datetime'] = pd.to_datetime(df_meter['Datetime'], utc=True)
        df_meter = df_meter[(df_meter['Datetime'] >= pd.to_datetime(start_datetime_object, utc=True)) &
                            (df_meter['Datetime'] <= pd.to_datetime(end_datetime_object, utc=True))]
        df_meter = f(df_meter)

        # df_meter['Date'] = df_meter.Datetime.apply(lambda d: d.split(" ", 1)[0])
        if value == 'TC':
            if selected_value == 'week':
                df_selected = df_meter[df_meter['Year'].isin(year)]
                df_selected = df_selected[df_selected['Week'].isin(week)]
                df_selected = df_selected.groupby("Year-Week").agg(
                    {'Hour': 'count', 'Actual': 'sum', 'Predicted': 'sum'}).reset_index()
                x = df_selected["Year-Week"]
            elif selected_value == 'day':
                df_selected = df_meter.groupby(["Date"]).sum().reset_index()
                x = df_selected["Date"]
            elif selected_value == 'hour':
                df_selected = df_meter
                x = df_selected["Hour"]
            elif selected_value == 'month':
                df_selected = df_meter.groupby(["Month"]).sum().reset_index()
                x = df_selected["Month"]
            else:
                df_selected = df_meter.groupby(["Year"]).sum().reset_index()
                x = df_selected["Year"]
        else:
            if selected_value == 'week':
                df_selected = df_meter[df_meter['Year'].isin(year)]
                df_selected = df_selected[df_selected['Week'].isin(week)]
                df_selected = df_selected.groupby("Year-Week").agg(
                    {'Hour': 'count', 'Actual': 'mean', 'Predicted': 'mean'}).reset_index()
                x = df_selected["Year-Week"]
            elif selected_value == 'day':
                df_selected = df_meter.groupby(["Date"]).mean().reset_index()
                x = df_selected["Date"]
            elif selected_value == 'hour':
                df_selected = df_meter
                x = df_selected["Hour"]
            elif selected_value == 'month':
                df_selected = df_meter.groupby(["Month"]).mean().reset_index()
                x = df_selected["Month"]
            else:
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
    return string_prefix, fig


if __name__ == '__main__':
    app.run_server(debug=True)
