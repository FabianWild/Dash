import os
import glob
import rasterio

# Input folder containing TIFF files
input_folder = 'assets/data'

# Output folder to save the downscaled TIFF files
output_folder = 'assets'

# Downsampling factor
downscale_factor = 2  # Adjust the value as desired

# Get a list of TIFF files in the input folder
tiff_files = glob.glob(os.path.join(input_folder, '*.tiff'))

for tiff_file in tiff_files:
    # Open the input TIFF file
    with rasterio.open(tiff_file) as src:
        # Calculate the new dimensions
        new_height = src.height // downscale_factor
        new_width = src.width // downscale_factor

        # Calculate the new transform
        new_transform = rasterio.transform.Affine(
            src.transform.a * downscale_factor,
            src.transform.b,
            src.transform.c,
            src.transform.d,
            src.transform.e * downscale_factor,
            src.transform.f
        )

        # Create the output file path
        output_file = os.path.join(output_folder, os.path.basename(tiff_file))

        # Configure the output TIFF file
        profile = src.profile
        profile.update(
            transform=new_transform,
            height=new_height,
            width=new_width
        )

        # Open the output TIFF file for writing
        with rasterio.open(output_file, 'w', **profile) as dst:
            # Perform the downsampling by reading and writing blocks
            for ji, window in dst.block_windows(1):
                src_data = src.read(window=window, masked=True)
                dst_data = src_data[:, ::downscale_factor, ::downscale_factor]
                dst.write(dst_data, window=window)

        print(f"Downsampling complete for: {tiff_file}")
