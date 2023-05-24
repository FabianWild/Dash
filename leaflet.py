import dash
from dash import html
import dash_leaflet as dl
import datetime
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import io
from io import BytesIO

app = dash.Dash(__name__)
app.title = "Dashboard zur Visualisierung von Fernerkundungsdaten"
app.layout = html.Div([
    html.H1('Multiple Leaflet Maps'),
    html.Div([
        dl.Map([
            dl.TileLayer(),
            dl.WMSTileLayer(
                url='https://services.sentinel-hub.com/ogc/wms/f9cfc572-6834-40de-b93c-72e01194d954',
                layers='NDVI',
                format='image/png',
                transparent=True
            )
        ], id='map1', zoom = 10, minZoom = 10, style={'height': '400px'}),
        html.Div(style={'height': '5px'}),  # Add spacing between map
        dl.Map([
            dl.TileLayer(),
            dl.WMSTileLayer(
                url='https://services.sentinel-hub.com/ogc/wms/f9cfc572-6834-40de-b93c-72e01194d954',
                layers='NDVI',
                format='image/png',
                transparent=True
            )
        ], id='map2', zoom = 10, minZoom = 10, style={'height': '400px'})
    ], style={"width": "40%", 'height': '50vh', "margin": "5px 5px 5px 5px", "justify-content": 'space-between'})
])

# Callback to synchronize map center and zoom
@app.callback(
    dash.dependencies.Output('map1', 'center'),
    dash.dependencies.Output('map2', 'center'),
    dash.dependencies.Output('map1', 'zoom'),
    dash.dependencies.Output('map2', 'zoom'),
    [dash.dependencies.Input('map1', 'center'),
     dash.dependencies.Input('map2', 'center'),
     dash.dependencies.Input('map1', 'zoom'),
     dash.dependencies.Input('map2', 'zoom')]
)
def update_map(map1_center, map2_center, map1_zoom, map2_zoom):
    new_center = map1_center if map1_center is not None else map2_center
    new_zoom = map1_zoom if map1_zoom is not None else map2_zoom
    return new_center, new_center, new_zoom, new_zoom


@app.callback(
    dash.dependencies.Output('map1', 'bounds'),
    dash.dependencies.Output('map2', 'bounds'),
    [dash.dependencies.Input('map1', 'click_lat_lng'),
     dash.dependencies.Input('map2', 'click_lat_lng')]
)
def update_map_bounds(map1_click, map2_click):
    return map1_click, map2_click

@app.callback(
    dash.dependencies.Output('map1', 'children'),
    dash.dependencies.Output('map2', 'children'),
    [dash.dependencies.Input('map1', 'bounds'),
     dash.dependencies.Input('map2', 'bounds')]
)
def update_map_layers(map1_bounds, map2_bounds):
    date = datetime.date(2022, 1, 23)  # Replace with your desired date

    url = 'https://services.sentinel-hub.com/ogc/wms/f9cfc572-6834-40de-b93c-72e01194d954'
    layer_params = {
        'service': 'WMS',
        'request': 'GetMap',
        'layers': 'NDVI',
        'format': 'image/png',
        'transparent': True,
        'width': 1000,
        'height': 1000,
        'bbox': f'{map1_bounds[0]},{map1_bounds[1]},{map1_bounds[2]},{map1_bounds[3]}' if map1_bounds else '',
        'time': date.strftime('%Y-%m-%d')
    }



    # """ wms_layer1 = dl.WMSTileLayer(
    #     url=url,
    #     layers='NDVI-S2-L1C',
    #     format='image/png',
    #     transparent=True,
    #     opacity=0.7,
    #     attribution='NDVI'
    # )

    # wms_layer1.image = ndvi

    # wms_layer2 = dl.WMSTileLayer(
    #     url=url,
    #     layers='NDVI-S2-L1C',
    #     format='image/png',
    #     transparent=True,
    #     opacity=0.7,
    #     attribution='NDVI'
    # )

    # wms_layer2.image = ndvi

    # return wms_layer1, wms_layer2 """

if __name__ == '__main__':
    app.run_server(debug=True)