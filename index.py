from dash import Input, Output, State, html, dcc
import dash_bootstrap_components as dbc
import dash
import json
# import bfabric
from utils import auth_utils, components

####### Main components of a Dash App: ########
# 1) app (dash.Dash())
# 2) app.layout (html.Div())
# 3) app.callback()

#################### (1) app ####################
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)

#################### (2) app.layout ####################

app.layout = html.Div(
    children=[
        dcc.Location(
            id='url',
            refresh=False
        ),
        dbc.Container(
            children=[    
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            className="banner",
                            children=[
                                html.Div(
                                    children=[
                                        html.P(
                                            'B-Fabric App Template',
                                            style={'color':'#ffffff','margin-top':'15px','height':'80px','width':'100%',"font-size":"40px","margin-left":"20px"}
                                        )
                                    ],
                                    style={"background-color":"#000000", "border-radius":"10px"}
                                ),
                            ],
                        ),
                    ),
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            children=[html.P(id="page-title",children=[str("Bfabric App Template")], style={"font-size":"40px", "margin-left":"20px", "margin-top":"10px"})],
                            style={"margin-top":"0px", "min-height":"80px","height":"6vh","border-bottom":"2px solid #d4d7d9"}
                        )
                    )
                ),
                dbc.Row(
                    id="page-content-main",
                    children=[
                        dbc.Col(
                            html.Div(
                                id="sidebar",
                                children=components.default_sidebar,
                                style={"border-right": "2px solid #d4d7d9", "height": "100%", "padding": "20px", "font-size": "20px"}
                            ),
                            width=3,
                        ),
                        dbc.Col(
                            html.Div(
                                id="page-content",
                                children=components.no_auth + [html.Div(id="auth-div")],style={"margin-top":"20vh", "margin-left":"2vw", "font-size":"20px"},
                            ),
                            width=9,
                        ),
                    ],
                    style={"margin-top": "0px", "min-height": "40vh"}
                ),
            ], style={"width":"100vw"},  
            fluid=True
        ),
        dcc.Store(id='token', storage_type='session'), # Where we store the actual token
        dcc.Store(id='entity', storage_type='session'), # Where we store the entity data retrieved from bfabric
        dcc.Store(id='token_data', storage_type='session'), # Where we store the token auth response
    ],style={"width":"100vw", "overflow-x":"hidden", "overflow-y":"scroll"}
)


#################### (3) app.callback ####################
@app.callback(
    [
        Output('token', 'data'),
        Output('token_data', 'data'),
        Output('entity', 'data'),
        Output('page-content', 'children'),
        Output('page-title', 'children'),
        Output('sidebar_text', 'hidden'),
        Output('example-slider', 'disabled'),
        Output('example-dropdown', 'disabled'),
        Output('example-input', 'disabled'),
        Output('example-button', 'disabled'),
    ],
    [
        Input('url', 'search'),
    ]
)
def display_page(url_params):
    
    base_title = "Bfabric App Template"

    if not url_params:
        return None, None, None, components.no_auth, base_title, True, True, True, True, True
    
    token = "".join(url_params.split('token=')[1:])
    tdata_raw = auth_utils.token_to_data(token)
    
    if tdata_raw:
        if tdata_raw == "EXPIRED":
            return None, None, None, components.expired, base_title, True, True, True, True, True

        else: 
            tdata = json.loads(tdata_raw)
    else:
        return None, None, None, components.no_auth, base_title, True, True, True, True, True
    
    if tdata:
        entity_data = json.loads(auth_utils.entity_data(tdata))
        page_title = f"{base_title} - {tdata['entityClass_data']} - {tdata['entity_id_data']} ({tdata['environment']} System)" if tdata else "Bfabric App Interface"

        if not tdata:
            return token, None, None, components.no_auth, page_title, True, True, True, True, True
        
        elif not entity_data:
            return token, None, None, components.no_entity, page_title, True, True, True, True, True
        
        else:
            return token, tdata, entity_data, components.auth, page_title, False, False, False, False, False
    else: 
        return None, None, None, components.no_auth, base_title, True, True, True, True, True
    
@app.callback(
    Output('auth-div', 'children'),
    [
        Input('example-slider', 'value'),
        Input('example-dropdown', 'value'),
        Input('example-input', 'value'),
        Input('example-button', 'n_clicks')
    ],
    [
        State('entity', 'data'),
        State('token_data', 'data'),
    ]
)
def update_auth_div(slider_val, dropdown_val, input_val, n_clicks, entity_data, token_data):

    if not entity_data or not token_data:
        return None

    entity_details = [
        html.H1(f"Entity Data:  "),
        html.P(f"Entity Class: {token_data['entityClass_data']}"),
        html.P(f"Entity ID: {token_data['entity_id_data']}"),
        html.P(f"Created By: {entity_data['createdby']}"),
        html.P(f"Created: {entity_data['created']}"),
        html.P(f"Modified: {entity_data['modified']}"),
    ]

    output = dbc.Row(
        [
            dbc.Col(
                [
                    html.H1("Component Data: "),
                    html.P(f"Slider Value: {slider_val}"),
                    html.P(f"Dropdown Value: {dropdown_val}"),
                    html.P(f"Input Value: {input_val}"),
                    html.P(f"Button Clicks: {n_clicks}")
                ]
            ),
            dbc.Col(
                entity_details
            )
        ]
    )

    return output


if __name__ == '__main__':
    app.run_server(debug=True, port=8050, host='localhost')