# import packages
from dash import Dash, html, dcc, Input, Output, State
import dash_leaflet as dl
import functions
from datetime import date, timedelta
from pathlib import Path
import rasterio
import numpy as np
import plotly.express as px
from flask import Flask, render_template


innsbruck = (47.267222, 11.392778)

# Get GeoTIFF information
with rasterio.open(r'assets/data/2022-01-13_B01.tiff') as fobj:
    array = fobj.read(1)
    bounds = fobj.bounds
    height = fobj.height
    width = fobj.width

# Define image bounds with extent
image_bounds = [[bounds.bottom, bounds.left],[bounds.top, bounds.right]]

# Calculate Resolution
x_res = (bounds.right-bounds.left)/width
y_res = (bounds.top-bounds.bottom)/height
days = ['2022-01-13', '2022-02-12', '2022-03-14', '2022-04-18', '2022-05-11', '2022-06-27', '2022-07-17', '2022-08-14', '2022-09-23', '2022-10-05', '2022-11-27', '2022-12-22']

# define disabled days
start_date = date(2022, 1, 1)
end_date = date(2022, 12, 31)
delta = timedelta(days=1)
able_days = [date(2022, 1, 13), date(2022, 2, 12), date(2022, 3, 14), date(2022, 4, 18), date(2022, 5, 11), date(2022, 6, 27), date(2022, 7, 17), date(2022, 8, 14), date(2022, 9, 23), date(2022, 10, 5), date(2022, 11, 27), date(2022, 12, 22),]
disabled_days = []
while start_date <= end_date:
    if start_date in able_days:
        start_date += delta
        continue
    # add current date to list
    disabled_days.append(start_date)
    # increment start date by timedelta
    start_date += delta

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)
server = app.server

# Defining app layout
app.title = "Dashboard zur Visualisierung von Fernerkundungsdaten"
app.layout = html.Div(children=[
    html.Div(className='row', children=[
        html.H1('Dashboard zur Visualisierung von Fernerkundungsdaten'),
        html.Hr(),
        html.P('Vergleichen von verschiedenen Indizes für die Region Innsbruck. Auswählen von verschiedenen Layern möglich. Durch Klick auf Karte können Indizes für eine bestimmte Position geplottet werden.')
    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.DatePickerSingle(
                id='my-date-picker-single-1',  # Unique ID for the first DatePickerSingle
                min_date_allowed=date(2022, 1, 1),
                max_date_allowed=date(2022, 12, 31),
                initial_visible_month=date(2022, 1, 13),
                date=date(2022, 1, 13),
                disabled_days=disabled_days,
                style={'position': 'relative', 'zIndex': 9999}
            ),
            html.Div(style={'height': '2px'}),
            dl.Map([
                dl.LayersControl(
                    [dl.BaseLayer(dl.TileLayer(), name='osm', checked=True)] +
                    [dl.Overlay(
                        dl.ImageOverlay(
                            id='timelayer1',
                            url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_True_color.jpg', bounds=image_bounds, opacity=1), name='RGB'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_falsecolor", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_False_color.jpg', bounds=image_bounds, opacity=1), name='False Color'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_moisture", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_Moisture_index.jpg', bounds=image_bounds, opacity=1), name='Moisture Index'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_NDSI", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_NDSI.jpg', bounds=image_bounds, opacity=1), name='NDSI'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_NDVI", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_NDVI.jpg', bounds=image_bounds, opacity=1), name='NDVI'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_NDWI", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI')
                    ]
                ),
                dl.LayerGroup(id="click1")
            ], style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"}, 
            center=innsbruck, 
            zoom=12, 
            id='map1', 
            maxBounds=image_bounds,  # Restrict zoom and pan functionality to image_bounds
            minZoom=11
            ),
            html.Div(style={'height': '10px'}),
            html.Div(id='dropdown1'),
            html.Div(id='timeseries1')
        ]),
        html.Div(className='six columns', children=[
            dcc.DatePickerSingle(
                id='my-date-picker-single-2',  # Unique ID for the second DatePickerSingle
                min_date_allowed=date(2022, 1, 1),
                max_date_allowed=date(2022, 12, 31),
                initial_visible_month=date(2022, 1, 13),
                date=date(2022, 1, 13),
                disabled_days=disabled_days,
                style={'position': 'relative', 'zIndex': 9999}
            ),
            html.Div(style={'height': '2px'}),
            dl.Map([
                dl.LayersControl(
                    [dl.BaseLayer(dl.TileLayer(), name='osm', checked=True)] +
                    [dl.Overlay(
                        dl.ImageOverlay(
                            id='timelayer2',
                            url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_True_color.jpg', bounds=image_bounds, opacity=1), name='RGB'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_falsecolor2", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_False_color.jpg', bounds=image_bounds, opacity=1), name='False Color'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_moisture2", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_Moisture_Index.jpg', bounds=image_bounds, opacity=1), name='Moisture Index'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_NDSI2", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_NDSI.jpg', bounds=image_bounds, opacity=1), name='NDSI'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_NDVI2", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_NDVI.jpg', bounds=image_bounds, opacity=1), name='NDVI'),
                     dl.Overlay(dl.ImageOverlay(id = "timelayer_NDWI2", url='https://dash-leaflet.s3.amazonaws.com/assets/images/2022-01-13_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI')]
                ),
                dl.LayerGroup(id="click2")
            ], style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"}, 
            center=innsbruck, 
            zoom=12, 
            id='map2',
            maxBounds=image_bounds,  # Restrict zoom and pan functionality to image_bounds
            minZoom=11
            ),
            html.Div(style={'height': '10px'}),
            html.Div(id='dropdown2'),
            html.Div(id='timeseries2')
        ]),
    ]),
])

# Define callback for the first DatePickerSingle
@app.callback(
    [
        Output('timelayer1', 'url'),
        Output('timelayer_falsecolor', 'url'),
        Output('timelayer_moisture', 'url'),
        Output('timelayer_NDSI', 'url'),
        Output('timelayer_NDVI', 'url'),
        Output('timelayer_NDWI', 'url'),
    ],
    [
        Input('my-date-picker-single-1', 'date')
    ]
)
def update_map1(date_selected):
    # Generate the image URL based on the selected date
    rgb_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_True_color.jpg"
    false_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_False_color.jpg"
    moisture_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_Moisture_index.jpg"
    NDSI_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_NDSI.jpg"
    NDVI_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_NDVI.jpg"
    NDWI_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_NDWI.jpg"
    return rgb_url, false_url, moisture_url, NDSI_url, NDVI_url, NDWI_url

# Define callback for the second DatePickerSingle
@app.callback(
    [
        Output('timelayer2', 'url'),
        Output('timelayer_falsecolor2', 'url'),
        Output('timelayer_moisture2', 'url'),
        Output('timelayer_NDSI2', 'url'),
        Output('timelayer_NDVI2', 'url'),
        Output('timelayer_NDWI2', 'url'),
    ],
    [
        Input('my-date-picker-single-2', 'date')
    ]
)
def update_map2(date_selected):
    # Generate the image URL based on the selected date
    rgb_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_True_color.jpg"
    false_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_False_color.jpg"
    moisture_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_Moisture_index.jpg"
    NDSI_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_NDSI.jpg"
    NDVI_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_NDVI.jpg"
    NDWI_url = f"https://dash-leaflet.s3.amazonaws.com/assets/images/{date_selected}_NDWI.jpg"
    return rgb_url, false_url, moisture_url, NDSI_url, NDVI_url, NDWI_url


@app.callback(
    [
        Output('click1', 'children'),
        Output('dropdown1', 'children')
    ],
    [
        Input('map1', 'click_lat_lng'),
    ],
    [
        State('dropdown1', 'value')
    ]
)
def map_click(click_lat_lng, dropdown_value):
    return [dl.Marker(id='marker1', position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))], [html.P('Index für Zeitreihe wählen'), dcc.Dropdown(
        id='dropdown1',
        options=[
            {'label': 'Moisture Index', 'value': '*Moisture_index.tiff'},
            {'label': 'NDSI', 'value': '*NDSI.tiff'},
            {'label': 'NDVI', 'value': '*NDVI.tiff'},
            {'label': 'NDWI', 'value': '*NDWI.tiff'}
        ],
        value=dropdown_value,
        style={"width": "200px", "margin-bottom": "10px"}
    )]

@app.callback(
    [
        Output('click2', 'children'),
        Output('dropdown2', 'children')
    ],
    [
        Input('map2', 'click_lat_lng'),
    ],
    [
        State('dropdown2', 'value')
    ]
)
def map_click2(click_lat_lng, dropdown_value):
    return [dl.Marker(id='marker2', position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))], [html.P('Index für Zeitreihe wählen'), dcc.Dropdown(
        id='dropdown2',
        options=[
            {'label': 'Moisture Index', 'value': '*Moisture_index.tiff'},
            {'label': 'NDSI', 'value': '*NDSI.tiff'},
            {'label': 'NDVI', 'value': '*NDVI.tiff'},
            {'label': 'NDWI', 'value': '*NDWI.tiff'}
        ],
        value=dropdown_value,
        style={"width": "200px", "margin-bottom": "10px"}
    )]


# Define Callback for first time series
@app.callback(
    Output('timeseries1', 'children'),
    [
        Input('dropdown1', 'value'),
        Input('marker1', 'position')
    ]
)

def timeseries (index, lat_lng):
    # read in all files for chosen index
    file_path = Path('assets/data')
    bands = []
    for band in file_path.glob(index):
        band_array = functions.read_file(band)
        bands.append(band_array)

    # stack bands
    band_stack = np.dstack(bands)

    # get cell for coordinates
    y_cell = round((bounds.top-lat_lng[0])/y_res)
    x_cell = round((lat_lng[1]-bounds.left)/x_res)

    # create figure
    split_index = index.split('.')
    fig = px.line(x=days, y=band_stack[y_cell,x_cell,:])
    fig.update_xaxes(title = '')
    fig.update_yaxes(title = f'{split_index[0][1:]}')
    
    return [dcc.Graph(figure = fig)]

# Define Callback for second time series
@app.callback(
    Output('timeseries2', 'children'),
    [
        Input('dropdown2', 'value'),
        Input('marker2', 'position')
    ]
)

def timeseries (index, lat_lng):
    # read in all files for chosen index
    file_path = Path('assets/data')
    bands = []
    for band in file_path.glob(index):
        band_array = functions.read_file(band)
        bands.append(band_array)

    # stack bands
    band_stack = np.dstack(bands)

    # get cell for coordinates
    y_cell = round((bounds.top-lat_lng[0])/y_res)
    x_cell = round((lat_lng[1]-bounds.left)/x_res)

    # create figure
    split_index = index.split('.')
    fig = px.line(x=days, y=band_stack[y_cell,x_cell,:])
    fig.update_xaxes(title = '')
    fig.update_yaxes(title = f'{split_index[0][1:]}')
    
    return [dcc.Graph(figure = fig)]

if __name__ == '__main__':
    app.run_server(debug=True)
