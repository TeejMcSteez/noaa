from typing import cast

import pandas

from noaa.data import get_data

data = get_data("datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv")

data = cast(pandas.DataFrame, data)

if data is FileNotFoundError:
    raise FileNotFoundError
else:
    print(data["CZ_TIMEZONE"])
    print(data["BEGIN_DATE_TIME"])
    print(data["END_DATE_TIME"])
