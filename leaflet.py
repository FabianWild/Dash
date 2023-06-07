import dash
from dash import html, dcc
import dash_leaflet as dl

app = dash.Dash(__name__)
server = app.server

app.config.suppress_callback_exceptions = True

app.title = "Dashboard zur Visualisierung von Fernerkundungsdaten"
app.layout = html.Div(
    [
        html.H1('Multiple Leaflet Maps'),
        html.Div(
            [
                html.Label('Choose Layer:'),
                dcc.Dropdown(
                    id='layer-dropdown',
                    options=[
                        {'label': 'NDVI', 'value': 'NDVI'},
                        {'label': 'RGB', 'value': 'NATURAL-COLOR'},
                        {'label': 'FALSE-COLOR', 'value': 'FALSE-COLOR'}
                    ],
                    value='NDVI',
                    style={"width": "200px", "margin-bottom": "10px"}
                )
            ]
        ),
        html.Div(
            [
                dl.Map(
                    [
                        dl.TileLayer(),
                        dl.WMSTileLayer(
                            id='wms-layer1',
                            url='https://services.sentinel-hub.com/ogc/wms/f9cfc572-6834-40de-b93c-72e01194d954',
                            layers='NDVI',
                            format='image/png',
                            transparent=True
                        )
                    ],
                    id='map1',
                    zoom=10,
                    minZoom=10,
                    dragging=True,  # Enable map panning
                    style={'height': '400px'}
                ),
                html.Div(style={'height': '5px'}),  # Add spacing between maps
                dl.Map(
                    [
                        dl.TileLayer(),
                        dl.WMSTileLayer(
                            id='wms-layer2',
                            url='https://services.sentinel-hub.com/ogc/wms/f9cfc572-6834-40de-b93c-72e01194d954',
                            layers='NDVI',
                            format='image/png',
                            transparent=True
                        )
                    ],
                    id='map2',
                    zoom=10,
                    minZoom=10,
                    dragging=True,  # Enable map panning
                    style={'height': '400px'}
                )
            ],
            style={"width": "40%", 'height': '50vh', "margin": "5px 5px 5px 5px", "justify-content": 'space-between'}
        ),
    ]
)


@app.callback(
    [
        dash.dependencies.Output('wms-layer1', 'layers'),
        dash.dependencies.Output('wms-layer2', 'layers'),
        dash.dependencies.Output('map1', 'center'),
        dash.dependencies.Output('map2', 'center'),
        dash.dependencies.Output('map1', 'zoom'),
        dash.dependencies.Output('map2', 'zoom'),
    ],
    [
        dash.dependencies.Input('layer-dropdown', 'value'),
        dash.dependencies.Input('map1', 'center'),
        dash.dependencies.Input('map1', 'zoom'),
    ]
)
def update_maps(layer, map1_center, map1_zoom):
    wms_layer1 = layer
    wms_layer2 = layer
    map1_center = map1_center
    map2_center = map1_center
    map2_zoom = map1_zoom

    return wms_layer1, wms_layer2, map1_center, map2_center, map1_zoom, map2_zoom


if __name__ == '__main__':
    app.run_server(debug=True)
