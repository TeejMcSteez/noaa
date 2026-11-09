from typing import cast

import pandas

from noaa.data import get_data

data = get_data("datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv")

offsets = {
    "CST": "-0600",
    "EST": "-0500",
    "MST": "-0700",
    "PST": "-0800",
    "AST": "-0400",
    "HST": "-1000",
    "AKST": "-0900",
}

data = cast(pandas.DataFrame, data)

if data is FileNotFoundError:
    raise FileNotFoundError
else:
    # Extract D-M-Y TS from dates to add full year for accuracy
    dates = data["BEGIN_DATE_TIME"].str.extract(
        r"(\d{1,2})-([A-Za-z]{3})-(\d{2}) (\d{2}:\d{2}:\d{2})"
    )
    dates[2] = "19" + dates[2]
    print(dates)
    # Flip to Y-M-D TS adding 19 to the year (for this dataset only)
    data["BEGIN_DATE_TIME"] = (
        dates[2] + "-" + dates[1] + "-" + dates[0] + " " + dates[3]
    )
    # Add timezone with offset for proper datetime processing
    dts = data["BEGIN_DATE_TIME"] + " " + data["CZ_TIMEZONE"].map(offsets.get)
    print(dts)
    # convert to UTC
    tz_map = pandas.to_datetime(arg=dts, utc=True, format="%Y-%b-%d %H:%M:%S %z")
    print(tz_map)
