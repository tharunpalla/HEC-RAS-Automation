from datetime import datetime
import os, requests


def get_current_data(date, leftlon, rightlon, toplat, bottomlat):
    destination = "C:/Users/chand/Downloads/HEC_DSS_Automation/Vortex/examples/src/main/jython/grib2/"
    missing_dates = []
    hour = 0

    current_hour = datetime.now().hour
    if current_hour % 6 != 0: current_hour -= current_hour % 6

    # Older dates
    if date.day < datetime.now().day:
        current_hour = 18

    while hour <= 60:
        # if hour % 3 == 0 and hour != 0:
        url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam_conusnest.pl?" \
              "file=nam.t{:02d}z.conusnest.hiresf{:02d}.tm00.grib2" \
              "&subregion=&lev_surface=on&var_APCP=on" \
              "&leftlon={:.2f}&rightlon={:.2f}&toplat={:.2f}&bottomlat={:.2f}&dir=%2Fnam.{:04d}{:02d}{:02d}" \
            .format(current_hour, hour, leftlon, rightlon, toplat, bottomlat, date.year, date.month, date.day)

        # filename = "GaugeCorr_QPE_01H_00.00_{:04d}{:02d}{:02d}-{:02d}0000.grib2" \
        #     .format(date.year, date.month, date.day, hour)

        filename = 'nam.t{:02d}z.conusnest.hiresf{:02d}.tm00.grib2'.format(current_hour, hour)

        try:
            fetched_request = requests.get(url)
        except Exception as e:
            print("Failed to fetch the file for the date : {} and hour: {}".format(date, hour))
            print(e)
            missing_dates.append(date)
        else:
            with open(destination + os.sep + filename, 'wb') as f:
                f.write(fetched_request.content)
            print("Successfully fetched the file for the date : {} and hour: {} from the URL: {}".format(date, hour,
                                                                                                         url))
        hour += 1


date = datetime(2022, 2, 15, 0, 0)
leftlon = -78.2
rightlon = -77.7
toplat = 35.6
bottomlat = 35.4
print("Getting ongoing data...\n")
get_current_data(date, leftlon, rightlon, toplat, bottomlat)
print("\nSuccessfully fetched ongoing data")
