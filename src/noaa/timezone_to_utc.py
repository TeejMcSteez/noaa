from typing import cast

import pandas

from noaa.data import get_data


def parse_timezones(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    Transforms date times to UTC standard
    TODO: Add parsing for end date time
    """
    offsets = {
        "CST": "-0600",
        "EST": "-0500",
        "MST": "-0700",
        "PST": "-0800",
        "AST": "-0400",
        "HST": "-1000",
        "AKST": "-0900",
    }
    assert data is not FileNotFoundError
    data = cast(pandas.DataFrame, data)

    # Extract D-M-Y TS from dates to add full year for accuracy
    dates = data["BEGIN_DATE_TIME"].str.extract(
        r"(\d{1,2})-([A-Za-z]{3})-(\d{2}) (\d{2}:\d{2}:\d{2})"
    )
    dates[2] = "19" + dates[2]
    # Flip to Y-M-D TS adding 19 to the year (for this dataset only)
    data["BEGIN_DATE_UTC"] = dates[2] + "-" + dates[1] + "-" + dates[0] + " " + dates[3]
    # Add timezone with offset for proper datetime processing
    dts = data["BEGIN_DATE_UTC"] + " " + data["CZ_TIMEZONE"].map(offsets.get)
    # convert to UTC
    data["BEGIN_DATE_UTC"] = pandas.to_datetime(
        arg=dts, utc=True, format="%Y-%b-%d %H:%M:%S %z"
    )
    return data


print(
    parse_timezones(
        cast(
            pandas.DataFrame,
            get_data("datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv"),
        )
    )
)
