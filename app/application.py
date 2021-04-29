import dash
import dash_core_components as dcc
import dash_auth
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash_html_components as html
from decouple import config
from scrapper.database.mysql import Database
from components.form import get_main_form
from components.calculator import calculate_price
import numpy as np

# Set connection to database
db = Database(config('db_host'), config('db_port'), config('db_database'), config('db_user'), config('db_password'))

# Wait until connection is available
if not db.test_connection():
    exit(0)


# authentication
VALID_USERNAME_PASSWORD_PAIRS = [(config('app_username'), config('app_password'))]

# Create dash components
app = dash.Dash(
    __name__,
    meta_tags=[{'name': 'viewport', 'content': 'width=device-width'}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Set authentication
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div('', style={'padding': 10}),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("appraise", href="#"))
        ],
        brand="immoscrapper",
        brand_href="#",
        color="primary",
        dark=True,
    ),
    html.Hr(),
    html.Div(
        html.Div(
            id='main_form',
            children=[get_main_form(db)],
            style={'width': '40%',
                       'margin': 'auto',
                       'border': '2px solid #000000',
                       'padding': 50,
                       'border-radius': '25px',
                       'background-color': '#ffffff'}
            ),
        style={'background-color': '#d3e0f5', 'padding': 80}
    ),
    html.Div(
        html.Div(
            id='div_price',
            children=
                [
                    html.H3('Your flat is worth...'),
                    html.H2(
                        "",
                        id='final_price'
                    )
                ],
                style={'width': '40%',
                       'margin': 'auto',
                       'border': '2px solid #000000',
                       'padding': 50,
                       'border-radius': '25px',
                       'background-color': '#ffffff'}
            ),
        style={'background-color': '#d3e0f5', 'padding': 80}
    )
])


@app.callback(
    Output("final_price", "children"),
    Input("submit_button", "n_clicks"),
    [State("main_form", "children")]
)
def show_price(n_clicks, form_components):
    price_currency = ""
    if n_clicks is not None:
        price = calculate_price(form_components)
        if price == -1:
            price_currency = "Please, fill up all the fields in the form."
        else:
            price_currency = str(f'{price.astype(int):,}') + " €"
    return price_currency


# Start service
if __name__ == "__main__":
    app.title = 'immoscrapper'
    app.run_server(host="0.0.0.0", port="8085", debug=True, use_reloader=False)
