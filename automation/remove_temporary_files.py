import os

path = 'C:/Users/chand/Downloads/HEC_DSS_Automation/Vortex/examples/src/main/jython/grib2/'

# filtered_files = [file for file in os.listdir(path) if file.endswith(".gbx9") or file.endswith(".ncx4") or file.endswith(".tmp")]
filtered_files = [file for file in os.listdir(path) if file.endswith(".gbx9") or file.endswith(".ncx4") or file.endswith(".grib2")]
print(filtered_files)
for file in filtered_files:
    path_to_file = os.path.join(path, file)
    os.remove(path_to_file)