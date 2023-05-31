import dash
from dash import html
import dash_leaflet as dl
import datetime
import requests

# Initializing the Dash Application
app = dash.Dash(__name__)
server=app.server

# Setting Up Application Configuration
app.config.suppress_callback_exceptions = True

# Defining Application Title and Layout
app.title = "Dashboard zur Visualisierung von Fernerkundungsdaten"
app.layout = html.Div([
    html.H1('Multiple Leaflet Maps'),
    html.Div([
        dl.Map([
            dl.TileLayer(),
            dl.WMSTileLayer(
                url='https://services.sentinel-hub.com/ogc/wms/f9cfc572-6834-40de-b93c-72e01194d954',
                layers='NATURAL-COLOR',
                format='image/png',
                transparent=True
            )
        ], id='map1', zoom = 10, minZoom = 10, style={'height': '400px'}),
        html.Div(style={'height': '5px'}),  # Add spacing between map
        dl.Map([
            dl.TileLayer(),
            dl.WMSTileLayer(
                url='https://services.sentinel-hub.com/ogc/wms/f9cfc572-6834-40de-b93c-72e01194d954',
                layers='FALSE-COLOR',
                format='image/png',
                transparent=True
            )
        ], id='map2', zoom = 10, minZoom = 10, style={'height': '400px'})
    ], style={"width": "40%", 'height': '50vh', "margin": "5px 5px 5px 5px", "justify-content": 'space-between'})
])

# Callback to synchronize map center and zoom
@app.callback(
    [dash.dependencies.Output('map1', 'center'),
     dash.dependencies.Output('map2', 'center'),
     dash.dependencies.Output('map1', 'zoom'),
     dash.dependencies.Output('map2', 'zoom')],
    [dash.dependencies.Input('map1', 'center'),
     dash.dependencies.Input('map2', 'center'),
     dash.dependencies.Input('map1', 'zoom'),
     dash.dependencies.Input('map2', 'zoom')]
)
def update_map(map1_center, map2_center, map1_zoom, map2_zoom):
    if map1_center and map2_center:
        new_center = map1_center
    elif map1_center:
        new_center = map1_center
    else:
        new_center = map2_center
        
    if map1_zoom and map2_zoom:
        new_zoom = map1_zoom
    elif map1_zoom:
        new_zoom = map1_zoom
    else:
        new_zoom = map2_zoom

    return new_center, new_center, new_zoom, new_zoom


if __name__ == '__main__':
    app.run_server(debug=True)