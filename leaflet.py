# import packages
from dash import Dash, html, dcc, Input, Output
import dash_leaflet as dl
import functions
from datetime import date, timedelta

app = Dash(__name__)
server = app.server

innsbruck = (47.267222, 11.392778)

# Open the GeoTIFF files
band, bounds = functions.read_file(r'assets\data\2022-01-13-00_00_2022-01-13-23_59_Sentinel-2_L2A_B01_(Raw).tiff')

# Define image bounds with extent
image_bounds = [[bounds.bottom, bounds.left],[bounds.top, bounds.right]]

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
                            url='assets/images/2022-01-13_True_color.jpg', bounds=image_bounds, opacity=1), name='RGB'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_False_color.jpg', bounds=image_bounds, opacity=1), name='False Color'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_Moisture_Index.jpg', bounds=image_bounds, opacity=1), name='Moisture Index'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_NDSI.jpg', bounds=image_bounds, opacity=1), name='NDSI'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_NDVI.jpg', bounds=image_bounds, opacity=1), name='NDVI'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI')]
                ),
                dl.LayerGroup(id="click1")
            ], style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"}, center=innsbruck, zoom=12, id='map1'),
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
                            url='assets/images/2022-01-13_True_color.jpg', bounds=image_bounds, opacity=1), name='RGB'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_False_color.jpg', bounds=image_bounds, opacity=1), name='False Color'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_Moisture_Index.jpg', bounds=image_bounds, opacity=1), name='Moisture Index'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_NDSI.jpg', bounds=image_bounds, opacity=1), name='NDSI'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_NDVI.jpg', bounds=image_bounds, opacity=1), name='NDVI'),
                     dl.Overlay(dl.ImageOverlay(url='assets/images/2022-01-13_NDWI.jpg', bounds=image_bounds, opacity=1), name='NDWI')]
                ),
                dl.LayerGroup(id="click2")
            ], style={'width': '100%', 'height': '70vh', 'margin': "auto", "display": "block"}, center=innsbruck, zoom=12, id='map2'),
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

# Define callback for first MapClick
@app.callback(
    Output('click1', 'children'),
    [
        Input('map1', 'click_lat_lng'),
    ]
)

def map_click(click_lat_lng):
    print(click_lat_lng)
    return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]


if __name__ == '__main__':
    app.run_server(debug=True)
