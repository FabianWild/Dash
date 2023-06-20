# import packages
import dash
from dash import Dash, html, dcc, Input, Output
import dash_leaflet as dl
import functions
from datetime import date

app = dash.Dash(__name__)
server = app.server

innsbruck = (47.267222, 11.392778)

# Open the GeoTIFF files
band, bounds = functions.read_file(r'assets\data\01_13\2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_B01_(Raw).tiff')

# Define image bounds with extent
image_bounds = [[bounds.bottom, bounds.left],[bounds.top, bounds.right]]

# Initialize the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, prevent_initial_callbacks=True)

# Defining app layout
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
                id='my-date-picker-single-1',  # Unique ID for the first DatePickerSingle
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
                     dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI')]
                )
            ], style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, center=innsbruck, zoom=12, id='map'),
        ]),
        html.Div(className='six columns', children=[
            dcc.DatePickerSingle(
                id='my-date-picker-single-2',  # Unique ID for the second DatePickerSingle
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
                            id='timelayer2',
                            url='assets/images/01_13/2022-01-13_True_color.jpg', bounds=image_bounds, opacity=1), name='RGB'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_False_color.jpg', bounds=image_bounds, opacity=1), name='False Color'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_Moisture_Index.jpg', bounds=image_bounds, opacity=1), name='Moisture Index'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDSI.jpg', bounds=image_bounds, opacity=1), name='NDSI'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDVI.jpg', bounds=image_bounds, opacity=1), name='NDVI'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/01_13/2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI')]
                )
            ], style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}, center=innsbruck, zoom=12, id='map2'),
        ]),
    ]),
])

# Define callback for the first DatePickerSingle
@app.callback(
    Output('timelayer1', 'url'),
    [Input('my-date-picker-single-1', 'date')]
)
def update_map1(date_selected):
    # Generate the image URL based on the selected date
    image_url = f"assets/images/{date_selected}_True_color.jpg"
    return image_url

# Define callback for the second DatePickerSingle
@app.callback(
    Output('timelayer2', 'url'),
    [Input('my-date-picker-single-2', 'date')]
)
def update_map2(date_selected):
    # Generate the image URL based on the selected date
    image_url = f"assets/images/{date_selected}_True_color.jpg"
    return image_url


if __name__ == '__main__':
    app.run_server(debug=True)
