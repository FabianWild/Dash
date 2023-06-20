# import packages
from dash import Dash, html, dcc, Input, Output, callback
import dash_leaflet as dl
import numpy as np
import rasterio
import functions
from datetime import date

innsbruck = (47.267222, 11.392778)

# Open the GeoTIFF files
band, bounds = functions.read_file(r'assets\data\01_13\2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_B01_(Raw).tiff')

# define image bounds with extent
image_bounds = [[bounds.bottom, bounds.left],[bounds.top, bounds.right]]

# initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

# defining app layout
app.title = "Dashboard zur Visualisierung von Fernerkundungsdaten"
app.layout = html.Div(children=[
    html.Div(className='row', children=[
        html.H1('Dashboard zur Visualisierung von Fernerkundungsdaten'),
        html.Hr(),
        html.P('Hier Erklärung für App')
    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                min_date_allowed=date(2022, 1, 1),
                max_date_allowed=date(2022, 12, 31),
                initial_visible_month=date(2022, 7, 17),
                date=date(2022, 7, 17)
            ),
            html.Div(style={'height': '2px'}),
            dl.Map([
                dl.LayersControl(
                [dl.BaseLayer(dl.TileLayer(), name='osm', checked=True)] +
                [dl.Overlay(
                    dl.ImageOverlay(
                        id='timelayer1',
                        url='assets/images/01_13/2022-01-13_True_color.jpg', bounds=image_bounds, opacity=1), name='RGB'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_False_color.jpg', bounds=image_bounds, opacity=1), name='False Color'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_Moisture_Index.jpg', bounds=image_bounds, opacity=1), name='Moisture Index'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDSI.jpg', bounds=image_bounds, opacity=1), name='NDSI'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDVI.jpg', bounds=image_bounds, opacity=1), name='NDVI'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_SWIR.jpg', bounds=image_bounds, opacity=1), name='SWIR'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_Scene_classification_map.jpg', bounds=image_bounds, opacity=1), name='SCL'),]
            ),
                dl.LayerGroup(id="layer1")
            ],
            id='map1',
            center=innsbruck,
            zoom=12,
            minZoom=10,
            dragging=True,  # Enable map panning
            style={'width': '700px', 'height': '500px'}
            )
        ]),
        html.Div(className='six columns', children=[
            dcc.DatePickerSingle(
                id='my-date-picker-single',
                min_date_allowed=date(2022, 1, 1),
                max_date_allowed=date(2022, 12, 31),
                initial_visible_month=date(2022, 7, 17),
                date=date(2022, 7, 17)
            ),
            html.Div(style={'height': '2px'}),
            dl.Map([
                dl.LayersControl(
                [dl.BaseLayer(dl.TileLayer(), name='osm', checked=True)] +
                [dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_True_color.jpg', bounds=image_bounds, opacity=1), name='RGB'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_False_color.jpg', bounds=image_bounds, opacity=1), name='False Color'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_Moisture_Index.jpg', bounds=image_bounds, opacity=1), name='Moisture Index'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDSI.jpg', bounds=image_bounds, opacity=1), name='NDSI'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDVI.jpg', bounds=image_bounds, opacity=1), name='NDVI'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_SWIR.jpg', bounds=image_bounds, opacity=1), name='SWIR'),
                dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_Scene_classification_map.jpg', bounds=image_bounds, opacity=1), name='SCL'),]
            ),
                dl.LayerGroup(id="layer2")
            ],
            id='map2',
            center=innsbruck,
            zoom=12,
            minZoom=10,
            dragging=True,  # Enable map panning
            style={'width': '700px', 'height': '500px'}
            )
        ])
    ])
])

@callback(
    [
        Output('layer1', 'children'),
        Output('timelayer1', 'url')
    ],
    [
        Input('map1', 'click_lat_lng'),
        Input('my-date-picker-single', 'date')
    ]
)

def map_click(click_lat_lng, date_value):
    print(click_lat_lng)
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        url_new = f'assets/images/01_13/{date_string}_True_color.jpg'
        print(url_new)
    return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))], url_new
    
# run the app
if __name__ == '__main__':
    app.run_server(debug=True)