import dash_bootstrap_components as dbc


def get_antiquities_list():
    antiquity_list = ['0-5', '5-10', '10-20', '20-30', '30-50', '50+']
    return antiquity_list


def get_location_list(db):
    query = 'SELECT DISTINCT location from properties where location like "%Barcelona%" and portal="pisos" order by location ASC'
    location_list = db.select_unique_query(query)
    return location_list


def get_condition_list():
    condition_list = ['new', 'very good', 'good', 'remodelled', 'to renovate']
    return condition_list


def get_swimming_pool_list():
    swimming_pool_list = ['no', 'communal', 'own']
    return swimming_pool_list


def get_garden_list():
    garden_list = ['no', 'communal', 'own']
    return garden_list


def get_facing_list():
    facing_list = ['North', 'Northeast', 'East', 'Southeast', 'South', 'Southwest', 'West', 'Northwest']
    return facing_list


def get_heating_list():
    heating_list = ['no', 'electric', 'natural gas']
    return heating_list


def get_air_conditioning_list():
    air_conditioning_list = ['cold', 'cold and heat', 'no']
    return air_conditioning_list


def get_energy_certificates_list():
    certificate_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    return certificate_list


def get_yes_no_options():
    yes_no_options = [
        {'label': 'Yes', 'value': 1},
        {'label': 'No', 'value': 0}
    ]
    return yes_no_options


def get_main_form(db):
    buy_or_rent = dbc.FormGroup(
        [
            dbc.Label("Buy or rent"),
            dbc.RadioItems(
                id="input_buy_or_rent",
                options=[
                    {"label": "buy", "value": "buy"},
                    {"label": "rent", "value": "rent"}
                ],
                inline=True
            )
        ]
    )
    squared_meters = dbc.FormGroup(
        [
            dbc.Label("Squared meters"),
            dbc.Input(type="number", id="input_sqm", placeholder="80")
        ]
    )
    n_rooms = dbc.FormGroup(
        [
            dbc.Label("Number of bedrooms"),
            dbc.Input(type="number", id="input_n_rooms", placeholder="2")
        ]
    )
    n_bathrooms = dbc.FormGroup(
        [
            dbc.Label("Number of bathrooms"),
            dbc.Input(type="number", id="input_n_bathrooms", placeholder="1")
        ]
    )
    location = dbc.FormGroup(
        [
            dbc.Label('Location'),
            dbc.Select(
                id="input_location",
                options=[{'label': i, 'value': i} for i in get_location_list(db)]
            )
        ]
    )
    energy_certificate = dbc.FormGroup(
        [
            dbc.Label('Energy certificate'),
            dbc.Select(
                id="input_energy_certificate",
                options=[{'label': i, 'value': i} for i in get_energy_certificates_list()]
            ),
            dbc.FormText("If you are not sure, select 'E'.")
        ]
    )
    floor = dbc.FormGroup(
        [
            dbc.Label("Floor"),
            dbc.Input(type="number", id="input_floor", placeholder="6", min=0)
        ]
    )
    antiquity = dbc.FormGroup(
        [
            dbc.Label('Antiquity (years)'),
            dbc.Select(
                id="input_antiquity",
                options=[{'label': i, 'value': i} for i in get_antiquities_list()]
            )
        ]
    )
    condition = dbc.FormGroup(
        [
            dbc.Label('Condition'),
            dbc.Select(
                id="input_condition",
                options=[{'label': i, 'value': i} for i in get_condition_list()]
            )
        ]
    )
    heating = dbc.FormGroup(
        [
            dbc.Label('Heating'),
            dbc.Select(
                id="input_heating",
                options=[{'label': i, 'value': i} for i in get_heating_list()]
            )
        ]
    )
    garage = dbc.FormGroup(
        [
            dbc.Label("Number of parking spots"),
            dbc.Input(type="number", id="input_garage", placeholder="1")
        ]
    )
    lift = dbc.FormGroup(
        [
            dbc.Label("Lift"),
            dbc.Select(
                id="input_lift",
                options=get_yes_no_options()
            ),
        ]
    )
    equipped_kitchen = dbc.FormGroup(
        [
            dbc.Label("Equipped kitchen"),
            dbc.Select(
                id="input_equipped_kitchen",
                options=get_yes_no_options()
            ),
        ]
    )
    air_conditioning = dbc.FormGroup(
        [
            dbc.Label('Air conditioning'),
            dbc.Select(
                id="input_air_conditioning",
                options=[{'label': i, 'value': i} for i in get_air_conditioning_list()]
            )
        ]
    )
    terrace = dbc.FormGroup(
        [
            dbc.Label('Terrace'),
            dbc.Select(
                id="input_terrace",
                options=get_yes_no_options()
            )
        ]
    )
    security_system = dbc.FormGroup(
        [
            dbc.Label('Security system'),
            dbc.Select(
                id="input_security_system",
                options=get_yes_no_options()
            )
        ]
    )
    facing = dbc.FormGroup(
        [
            dbc.Label('Facing'),
            dbc.Select(
                id="input_facing",
                options=[{'label': i, 'value': i} for i in get_facing_list()]
            ),
            dbc.FormText("Where is your balcony oriented to? If there is no balcony, select 'North'.")
        ]
    )
    swimming_pool = dbc.FormGroup(
        [
            dbc.Label('Swimming pool'),
            dbc.Select(
                id="input_swimming_pool",
                options=[{'label': i, 'value': i} for i in get_swimming_pool_list()]
            )
        ]
    )
    garden = dbc.FormGroup(
        [
            dbc.Label('Garden'),
            dbc.Select(
                id="input_garden",
                options=[{'label': i, 'value': i} for i in get_garden_list()]
            )
        ]
    )
    submit_button = dbc.Button("Submit", color="info", className="mr-1", id='submit_button',
                               style={'float': 'right',
                                      'padding-right': 20})

    form = dbc.Form(
        [
            buy_or_rent,
            squared_meters,
            n_rooms,
            n_bathrooms,
            location,
            energy_certificate,
            floor,
            antiquity,
            condition,
            heating,
            garage,
            lift,
            equipped_kitchen,
            air_conditioning,
            terrace,
            security_system,
            facing,
            swimming_pool,
            garden,
            submit_button
        ]
    )
    return form

