import rasterio
import functions

# get raster information
with rasterio.open(r'assets\data\2022-01-13_B01.tiff') as fobj:
    array = fobj.read(1)
    bounds = fobj.bounds
    height = fobj.height
    width = fobj.width
    crs = fobj.crs
    transform = fobj.transform

days = ['2022-01-13', '2022-02-12', '2022-03-14', '2022-04-18', '2022-05-11', '2022-06-27', '2022-07-17', '2022-08-14', '2022-09-23', '2022-10-05', '2022-11-27', '2022-12-22']

#calc moisture index (B8A-B11)/(B8A+B11)
for day in days:
    file_B8A = f'assets/data/{day}_B8A.tiff'
    file_B11 = f'assets/data/{day}_B11.tiff'
    outfile= f'assets/data/{day}_Moisture_index.tiff'
    band_B8A = functions.read_file(file_B8A)
    band_B11 = functions.read_file(file_B11)

    band_moisture_index = (band_B8A-band_B11)/(band_B8A+band_B11)

    with rasterio.open(
        outfile,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=array.dtype,
        crs=crs,
        transform=transform
    ) as dst:
        dst.write(band_moisture_index, 1)

# calc NDSI (B3 - B11)/(B3 + B11)
for day in days:
    file_B03 = f'assets/data/{day}_B03.tiff'
    file_B11 = f'assets/data/{day}_B11.tiff'
    outfile = f'assets/data/{day}_NDSI.tiff'
    band_B03 = functions.read_file(file_B03)
    band_B11 = functions.read_file(file_B11)

    band_ndsi = (band_B03-band_B11)/(band_B03+band_B11)

    with rasterio.open(
        outfile,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=array.dtype,
        crs=crs,
        transform=transform
    ) as dst:
        dst.write(band_ndsi, 1)

# calc NDVI (B8 - B4)/(B8 + B4)
for day in days:
    file_B08 = f'assets/data/{day}_B08.tiff'
    file_B04 = f'assets/data/{day}_B04.tiff'
    outfile = f'assets/data/{day}_NDVI.tiff'
    band_B08 = functions.read_file(file_B08)
    band_B04 = functions.read_file(file_B04)

    band_ndvi = (band_B08-band_B04)/(band_B08+band_B04)

    with rasterio.open(
        outfile,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=array.dtype,
        crs=crs,
        transform=transform
    ) as dst:
        dst.write(band_ndvi, 1)

# calc NDWI (B3 - B11)/(B3 + B11)
for day in days:
    file_B03 = f'assets/data/{day}_B03.tiff'
    file_B08 = f'assets/data/{day}_B08.tiff'
    outfile = f'assets/data/{day}_NDWI.tiff'
    band_B03 = functions.read_file(file_B03)
    band_B08 = functions.read_file(file_B08)

    band_ndwi = (band_B03-band_B08)/(band_B03+band_B08)

    with rasterio.open(
        outfile,
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=1,
        dtype=array.dtype,
        crs=crs,
        transform=transform
    ) as dst:
        dst.write(band_ndwi, 1)