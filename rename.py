import os

directory = 'assets/data'

# Get a list of all files in the specified directory
file_list = os.listdir(directory)
print(len(file_list))
# Iterate over each file
for filename in file_list:
    print(filename[0:10]+filename[48:52]+'.tiff')
    # Check if the file is an image
    if filename.lower().endswith(('.tiff')):
        # Construct the new file name
        new_filename = filename[0:10]+filename[48:52]+'.tiff'
        # Create the full path for the current file
        current_path = os.path.join(directory, filename)
        # Create the full path for the new file name
        new_path = os.path.join(directory, new_filename)
        # Rename the file
        os.rename(current_path, new_path)
        print(f"Renamed {filename} to {new_filename}")
