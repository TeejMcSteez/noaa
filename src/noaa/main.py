from datetime import datetime

from noaa.data import assign_split, get_data, norm_text, md5, get_bulk_data
from noaa.property_damage import parse_property_damage
from noaa.timezone_to_utc import parse_timezones
import pandas
from typing import cast

data = get_data("datasets/11-9-2026-google.csv")

assert data is not FileNotFoundError

data = cast(pandas.DataFrame, data)
data = parse_property_damage(data)
data = parse_timezones(data)
narr = norm_text(cast(pandas.Series, data["EPISODE_NARRATIVE"]))

data["group_key"] = (
    "ep:" + data["EPISODE_ID"].astype("Int64").astype(str)
).where(data["EPISODE_ID"].notna())

data["group_key"] = data["group_key"].fillna(
    ("narr:" + narr.map(md5)).where(narr != "")
)

data["group_key"] = data["group_key"].fillna("ev:" + data["EVENT_ID"].astype(str))

print(data["group_key"].map(assign_split))

data.to_csv(f"datasets/gen/output-{datetime.now()}.csv")
