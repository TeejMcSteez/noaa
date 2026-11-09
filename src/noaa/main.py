from noaa.data import assign_split, get_data, norm_text, md5
from noaa.property_damage import parse_property_damage
from noaa.timezone_to_utc import parse_timezones
from numpy._core.numeric import astype
import pandas
from typing import cast

data = get_data("datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv")

assert data is not FileNotFoundError

data = cast(pandas.DataFrame, data)
print(data)
data = parse_property_damage(data)
data = parse_timezones(data)
narr = norm_text(data["EPISODE_NARRATIVE"])

data["group_key"] = (
    "ep:" + data["EPISODE_ID"].astype("Int64").astype(str)
).where(data["EPISODE_ID"].notna())

data["group_key"] = data["group_key"].fillna(
    ("narr:" + narr.map(md5)).where(narr != "")
)

data["group_key"] = data["group_key"].fillna("ev:" + data["EVENT_ID"].astype(str))

print(data["group_key"].map(assign_split))
