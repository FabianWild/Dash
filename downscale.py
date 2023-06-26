import os
import rasterio

def downscale_tiff(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".tiff"):
            filepath = os.path.join(directory, filename)
            with rasterio.open(filepath) as src:
                profile = src.profile
                profile.update(
                    width=src.width // 2,
                    height=src.height // 2
                )
                data = src.read(
                    out_shape=(src.count, src.height // 2, src.width // 2),
                    resampling=rasterio.enums.Resampling.cubic
                )
            with rasterio.open(filepath, 'w', **profile) as dst:
                dst.write(data)
            print(f"{filename} has been downscaled and replaced.")

# Provide the directory path where the TIFF files are located
directory_path = "assets/data"

downscale_tiff(directory_path)
