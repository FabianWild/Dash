# Functions for dash
import rasterio

def read_file(filepath):
    with rasterio.open(filepath) as fobj:
        array = fobj.read(1)
        bounds = fobj.bounds

        return array, bounds