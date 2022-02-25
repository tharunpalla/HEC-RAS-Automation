import os
from os import listdir
from os.path import isfile, join

from mil.army.usace.hec.vortex.geo import WktFactory
from mil.army.usace.hec.vortex.io import BatchImporter


def convert_grib2_to_dss(in_files):
    # Variables for historical data
    # variables = ['GaugeCorrQPE01H_altitude_above_msl']

    # Variables for current data
    variables = ['Total_precipitation_surface_2_Hour_Accumulation', 'Total_precipitation_surface_1_Hour_Accumulation',
                 'Total_precipitation_surface_0_Hour_Accumulation', 'Total_precipitation_surface_3_Hour_Accumulation']

    # variables = ['Total_precipitation_surface_1_Hour_Accumulation']

    clip_shp = 'C:\Users\chand\Downloads\HEC_DSS_Automation\Vortex\examples\src\main\jython\shape.shp'

    geo_options = {
        'pathToShp': clip_shp,
        'targetCellSize': '2000',
        'targetWkt': WktFactory.shg(),
        'resamplingMethod': 'Bilinear'
    }

    destination = 'C:/Users/chand/Downloads/HEC_DSS_Automation/testing.dss'
    write_options = {'partF': 'my script import'}

    myImport = BatchImporter.builder() \
        .inFiles(in_files) \
        .variables(variables) \
        .geoOptions(geo_options) \
        .destination(destination) \
        .writeOptions(write_options) \
        .build()

    myImport.process()


path = 'C:/Users/chand/Downloads/HEC_DSS_Automation/Vortex/examples/src/main/jython/grib2/'
files = [f for f in listdir(path) if isfile(join(path, f))]
for i in range(len(files)):
    files[i] = path + files[i]
try:
    convert_grib2_to_dss(files)
except Exception as e:
    print("Exception occurred {} ".format(e))
finally:
    filtered_files = [file for file in os.listdir(path) if file.endswith(".gbx9") or file.endswith(".ncx4")]
    print(filtered_files)
    for file in filtered_files:
        path_to_file = os.path.join(path, file)
        os.remove(path_to_file)
