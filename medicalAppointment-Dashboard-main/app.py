import dash
import pandas as pd
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output
import plotly.express as px

def load_data():
    df = pd.read_csv("C:/Users/Mazen/Downloads/medicalAppointment-Dashboard-main/medicalAppointment-Dashboard-main/assets/cleanedMedicalAppointments.csv")
    df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'])
    df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'])
    return df


df = load_data()

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, './asstes/style.css'])

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H1("Medical Appointments Dashboard"), width=20, className="text-center")
    ], className="mb-5"),

    # Patients Demographics
    dbc.Row([
        dbc.Col(html.H2("1) Patient Demographics Summary"), className="main-title")
    ]),
    dbc.Row([
        # Gender Distribution BarChart
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Gender Distribution", className="card-title"),
                dcc.Dropdown(
                    id= "gender-filter",
                    options=[
                        {"label":"Male", "value":"M"},
                        {"label":"Female", "value": "F"}
                    ],
                    value=None,
                    placeholder="Select a gender"
                ),
                dcc.Graph(id="gender-dist")
            ])
        ]), width=6),
        # Age Distribution histogram
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Age Distribution", className="card-title"),
                dcc.Slider(
                    id="age-slider",
                    min=df["Age"].min(),
                    max=df["Age"].max(),
                    value=df["Age"].median(),
                    marks={int(value): f"{int(value)}" for value in df["Age"].quantile([0, .25, .50, .75, 1]).values},
                    step=5
                ),
                dcc.Graph(id="age-dist")
            ])
        ]), width=6),
        # Appointments by Neighbourhood BarChart
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Appointments by Neighbourhood", className="card-title"),
                dcc.Dropdown(
                    id= "neighbour-filter",
                    options=[{"label": neighbourhood, "value": neighbourhood} for neighbourhood in df['Neighbourhood'].unique()],
                    value=None,
                    placeholder="Select the Neighbourhood"
                ),
                dcc.Graph(id="appointNeigh-dist")
            ])
        ]), width=20)
    ], className="mb-5"),

    # Health Conditions Analysis
    dbc.Row([
        dbc.Col(html.H2("2) Health Conditions Analysis"), className="main-title")
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Health Condition vs No-Show", className="card-title"),
                dcc.Graph(id="condition-noshow")
            ])
        ]), width=12)
    ], className="mb-5"),

    # Appointment Behavior Analysis
    dbc.Row([
        dbc.Col(html.H2("3) Appointment Behavior Analysis", className="main-title"))
    ]),
    dbc.Row([
        dbc.Col(
            dcc.RadioItems(
                id="sms-filter",
                options=[
                    {"label": "No SMS", "value": 0},
                    {"label": "SMS Received", "value": 1}
                ],
                value=0,
                inline=True,
                labelStyle={"margin-right": "20px"}, 
                className="mb-3"
            )
        )
    ]),
    dbc.Row([
        # Waiting Time Histogram
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Waiting Time Distribution", className="card-title"),
                dcc.Graph(id="waitingtime-hist")
            ])
        ]), width=6),
        # No-Show by Waiting Time Category (Grouped Bar)
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("No-Show by Waiting Time Category", className="card-title"),
                dcc.Graph(id="waiting-cat-bar")
            ])
        ]), width=6),
        # Line chart - Appointments Over Time
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Appointments Over Time", className="card-title"),
                dcc.Graph(id="appointments-time-line")
            ])
        ]), width=12)

    ], className="mb-5"),
    
    # KPIs Section (Big Stat Cards)
    dbc.Row([
        dbc.Col(html.H2("4) No-show Rate Dashboard"), className="main-title")
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Appointments", className="card-title"),
                html.H2(id="total-appointments", className="card-text")
            ])
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total No-shows", className="card-title"),
                html.H2(id="total-no-shows", className="card-text")
            ])
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Show-up Rate (%)", className="card-title"),
                html.H2(id="show-up-rate", className="card-text")
            ])
        ]), width=3),
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Avg Waiting Time", className="card-title"),
                html.H2(id="avg-waiting-time", className="card-text")
            ])
        ]), width=3),
    ], className="mb-5"),

    # No Show by neighbourhood
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("No-show Rate by Neighbourhood", className="card-title"),
                dcc.Graph(id="noshow-neighbourhood")
            ])
        ]), width=12)
    ], className="mb-5"),

    # No Show by Age Gender
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("No-show Rate by Age & Gender", className="card-title"),
                dcc.Graph(id="noshow-age-gender")
            ])
        ]), width=12)
    ], className="mb-5")

])

# Callbacks
@app.callback(
    Output("gender-dist", "figure"),
    Input("gender-filter", "value")
)
def updateGenderDist(gender):
    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df

    fig = px.histogram(filtered_df, x="Gender", color="NoShow", barmode="group")

    return fig

@app.callback(
    Output("age-dist", "figure"),
    Input("age-slider", "value")
)
def updateAgeDist(selected_age):
    filtered_df = df[df["Age"] <= selected_age]
    fig = px.histogram(filtered_df, x="Age", color="NoShow", nbins=30, barmode="group")
    return fig

@app.callback(
    Output("appointNeigh-dist", "figure"),
    Input("neighbour-filter", "value")
)
def updateNeighDist(neigh):
    if neigh:
        filtered_df = df[df["Neighbourhood"] == neigh]
    else:
        filtered_df = df

    fig = px.histogram(filtered_df, x="Neighbourhood", color="NoShow", barmode="group")
    return fig

@app.callback(
    Output("condition-noshow", "figure"),
    Input("gender-filter", "value")  # Optional filtering
)
def update_condition_chart(gender):
    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df

    condition_vars = ["Hypertension", "Diabetes", "Alcoholism", "Handicap"]
    filtered_df = filtered_df.melt(id_vars=["NoShow"], value_vars=condition_vars, var_name="Condition", value_name="Present")
    filtered_df = filtered_df[filtered_df["Present"] == 1]
    fig = px.histogram(filtered_df, x="Condition", color="NoShow", barmode="group")
    return fig

# Waiting Time Histogram
@app.callback(
    Output("waitingtime-hist", "figure"),
    Input("sms-filter", "value")
)
def update_waiting_hist(sms_val):
    filtered_df = df[df["SMSReceived"] == sms_val]
    fig = px.histogram(filtered_df, x="WaitingDays", nbins=30, color="NoShow", barmode="group")
    return fig

# Waiting Time Category Bar Chart
@app.callback(
    Output("waiting-cat-bar", "figure"),
    Input("sms-filter", "value")
)
def update_waiting_cat(sms_val):
    filtered_df = df[df["SMSReceived"] == sms_val]
    bins = [-100, -1, 0, 5, 10, 20, 40, 100]
    labels = ["Past", "0", "1-5", "6-10", "11-20", "21-40", "40+"]
    filtered_df["WaitCat"] = pd.cut(filtered_df["WaitingDays"], bins=bins, labels=labels)
    fig = px.histogram(filtered_df, x="WaitCat", color="NoShow", barmode="group", category_orders={"WaitCat": labels})
    return fig

# Appointments Over Time Line Chart
@app.callback(
    Output("appointments-time-line", "figure"),
    Input("sms-filter", "value")
)
def update_time_line(sms_val):
    filtered_df = df[df["SMSReceived"] == sms_val]
    filtered_df["ScheduledDay"] = pd.to_datetime(filtered_df["ScheduledDay"])
    grouped = filtered_df.groupby(filtered_df["ScheduledDay"].dt.date)["NoShow"].value_counts().unstack().fillna(0)  # Divides the no show into yes and no columns
    grouped.index = pd.to_datetime(grouped.index)
    fig = px.line(grouped, x=grouped.index, y=grouped.columns, markers=True)
    return fig


@app.callback(
    Output("total-appointments", "children"),
    Output("total-no-shows", "children"),
    Output("show-up-rate", "children"),
    Output("avg-waiting-time", "children"),
    Input("sms-filter", "value")  # You can link this to a filter
)
def update_kpis(sms_val):
    dff = df[df["SMSReceived"] == sms_val]
    total = len(dff)
    no_shows = len(dff[dff["NoShow"] == "Yes"])
    show_rate = 100 * (1 - no_shows / total) if total > 0 else 0
    avg_wait = dff["WaitingDays"].mean()
    return total, no_shows, f"{show_rate:.1f}%", f"{avg_wait:.1f} days"

@app.callback(
    Output("noshow-neighbourhood", "figure"),
    Input("gender-filter", "value")
)
def update_noshow_by_neighbourhood(gender):
    if gender:
        filtered_df = df[df["Gender"] == gender]
    else:
        filtered_df = df

    # Calculate no-show rate by neighbourhood
    grouped = filtered_df.groupby("Neighbourhood")["NoShow"].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).sort_values(ascending=False)

    fig = px.bar(
        grouped,
        x=grouped.index,
        y=grouped.values,
        labels={'x': 'Neighbourhood', 'y': 'No-show Rate (%)'},
        title="No-show Rate by Neighbourhood"
    )
    fig.update_layout(xaxis_tickangle=45)

    return fig


@app.callback(
    Output("noshow-age-gender", "figure"),
    Input("gender-filter", "value")  # Optional
)
def update_noshow_by_age_gender(gender):
    if gender:
        filtered_df = filtered_df[filtered_df["Gender"] == gender]
    else:
        filtered_df = df

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, filtered_df["Age"].max()]
    labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins) - 1)]
    filtered_df["AgeGroup"] = pd.cut(filtered_df["Age"], bins=bins, labels=labels, include_lowest=True)

    # Group by AgeGroup and Gender and calculate No-show Rate
    grouped = filtered_df.groupby(["AgeGroup", "Gender"])["NoShow"].apply(
        lambda x: (x == 'Yes').mean() * 100
    ).reset_index(name="NoShowRate")

    fig = px.bar(
        grouped,
        x="AgeGroup",
        y="NoShowRate",
        color="Gender",
        barmode="group",
        labels={"NoShowRate": "No-show Rate (%)"},
        title="No-show Rate by Age Group & Gender"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)