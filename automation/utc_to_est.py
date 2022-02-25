import os, eccodes, pytz
from datetime import datetime


def utc_to_est(time):
    year, month, day, hours, minutes, seconds = time[0], time[1], time[2], time[3], time[4], time[5]
    est = pytz.timezone('US/Eastern')
    utc = pytz.utc
    est_converted = datetime(year, month, day, hours, minutes, seconds, tzinfo=utc).astimezone(est)
    return [est_converted.year, est_converted.month, est_converted.day, est_converted.hour, est_converted.minute,
            est_converted.second]


INPUT_DIRECTORY = 'C:/Users/chand/Downloads/HEC_DSS_Automation/Vortex/examples/src/main/jython/grib2/'

# current_data
# keys = [['yearOfEndOfOverallTimeInterval', 'monthOfEndOfOverallTimeInterval', 'dayOfEndOfOverallTimeInterval',
#          'hourOfEndOfOverallTimeInterval', 'minuteOfEndOfOverallTimeInterval', 'secondOfEndOfOverallTimeInterval'],
#         ['year', 'month', 'day', 'hour', 'minute', 'second']]

# # #historical_data
keys = [['year', 'month', 'day', 'hour', 'minute', 'second']]

for file in os.scandir(INPUT_DIRECTORY):
    print("\nFile: ", file.path)
    with open(file.path) as f:
        gid = eccodes.codes_grib_new_from_file(f)
        for keyarr in keys:
            utc_time = []
            for key in keyarr:
                try:
                    val = eccodes.codes_get(gid, key)
                except Exception as e:
                    print("Error occurred while reading the key: ", key)
                    print(e)
                    val = 0
                finally:
                    utc_time.append(val)
            print(f'Keys: {keyarr}')
            print(f'Old values: {utc_time}')

            est_time = utc_to_est(utc_time)
            print(f'New values: {est_time}')

            for index, key in enumerate(keyarr):
                try:
                    eccodes.codes_set(gid, key, est_time[index])
                except Exception as e:
                    print("Error occurred while writing the key: ", key)
                    print(e)

            with open(file.path, "wb") as f:
                eccodes.codes_write(gid, f)
            print("Keys written successfully")
        eccodes.codes_release(gid)
