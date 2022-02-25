from datetime import datetime
from datetime import timedelta
import os, requests
import gzip
from shapely.geometry import Polygon
import geopandas as gpd


def get_historical_data(start, end):
    hour = timedelta(hours=1)
    destination = "C:/Users/chand/Downloads/HEC_DSS_Automation/Vortex/examples/src/main/jython/grib2/"
    date = start
    missing_dates = []
    fallback_to_radaronly = True
    while date <= end:
        url = "http://mtarchive.geol.iastate.edu/{:04d}/{:02d}/{:02d}/" \
              "mrms/ncep/GaugeCorr_QPE_01H/GaugeCorr_QPE_01H_00.00_{:04d}{:02d}{:02d}-{:02d}0000.grib2.gz" \
            .format(date.year, date.month, date.day, date.year, date.month, date.day, date.hour)
        filename = url.split("/")[-1]
        try:
            fetched_request = requests.get(url)
        except BaseException as e:
            missing_dates.append(date)
        else:
            with open(destination + os.sep + filename, 'wb') as f:
                f.write(fetched_request.content)
        finally:
            date += hour

    if fallback_to_radaronly:
        radar_also_missing = []
        for date in missing_dates:
            url = "http://mtarchive.geol.iastate.edu/{:04d}/{:02d}/{:02d}/" \
                  "mrms/ncep/RadarOnly_QPE_01H/RadarOnly_QPE_01H_00.00_{:04d}{:02d}{:02d}-{:02d}0000.grib2.gz" \
                .format(date.year, date.month, date.day, date.year, date.month, date.day, date.hour)
            filename = url.split("/")[-1]
            try:
                fetched_request = requests.get(url)
            except BaseException as e:
                radar_also_missing.append(date)
            else:
                with open(destination + os.sep + filename, 'wb') as f:
                    print("Fetched file with filename {}".format(filename))
                    f.write(fetched_request.content)


def make_output_path(output_directory, zipped_name):
    name_without_gzip_extension = zipped_name[:-len(GZIP_EXTENSION)]
    return os.path.join(output_directory, name_without_gzip_extension)


def generate_shape_file(left_long, right_long, bottom_lat, top_lat):
    lat_points = [bottom_lat, top_lat, top_lat, bottom_lat, bottom_lat]
    long_points = [left_long, left_long, right_long, right_long, left_long]

    bounds_geom = Polygon(zip(long_points, lat_points))
    print(bounds_geom)

    crs = "EPSG:4326"
    bounds_WGS = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[bounds_geom])
    bounds = bounds_WGS.to_crs("EPSG:5070")

    bounds.to_file(filename='shape.shp', driver="ESRI Shapefile")


# start = datetime(2016, 10, 8, 0, 0)
# end = datetime(2016, 10, 10, 0, 0)
start = datetime(2020, 6, 6, 0, 0)
end = datetime(2020, 6, 6, 23, 0)
print("Getting historical data")
get_historical_data(start, end)
print("Successfully fetched historical data")

print("Started unzipping gz files")
INPUT_DIRECTORY = 'C:/Users/chand/Downloads/HEC_DSS_Automation/Vortex/examples/src/main/jython/grib2/'
OUTPUT_DIRECTORY = INPUT_DIRECTORY
GZIP_EXTENSION = '.gz'

for file in os.scandir(INPUT_DIRECTORY):
    if not file.name.lower().endswith(GZIP_EXTENSION):
        continue
    output_path = make_output_path(OUTPUT_DIRECTORY, file.name)
    print('Decompressing the fetched files', file.path, 'to', output_path)
    with gzip.open(file.path, 'rb') as file:
        with open(output_path, 'wb') as output_file:
            output_file.write(file.read())

filtered_files = [file for file in os.listdir(INPUT_DIRECTORY) if file.endswith(".gz")]
print(filtered_files)
for file in filtered_files:
    path_to_file = os.path.join(INPUT_DIRECTORY, file)
    os.remove(path_to_file)

print('\nGenerating Shape File')
left_long = -78.2
right_long = -77.7
bottom_lat = 35.4
top_lat = 35.6
generate_shape_file(left_long, right_long, bottom_lat, top_lat)
print('\nSuccessfully generated shape file')
