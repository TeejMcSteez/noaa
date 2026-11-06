import pandas
from noaa.data import get_data

data = get_data("StormEvents_details-ftp_v1.0_d1950_c20260323.csv")

if data is FileNotFoundError:
    raise FileNotFoundError
else:
    tz_map = {

    }
