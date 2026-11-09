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
    # Add timezone with offset for proper datetime processing
    sts = data["BEGIN_DATE_TIME"] + " " + data["CZ_TIMEZONE"].map(offsets.get)
    ets = data["END_DATE_TIME"] + " " + data["CZ_TIMEZONE"].map(offsets.get)
    # convert to UTC
    data["BEGIN_DATE_UTC"] = pandas.to_datetime(
        arg=sts, utc=True, format="%Y-%b-%d %H:%M:%S %z"
    )
    data["END_DATE_UTC"] = pandas.to_datetime(
        args=ets, utc=True, format="%Y-%b-%d %H:%M:%S %z", errors="coerce"
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
