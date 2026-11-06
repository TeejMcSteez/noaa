from noaa.data import get_data
import pandas

data = get_data("datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv")

if data is FileNotFoundError:
    raise FileNotFoundError

mult = {"K": 1e3, "M": 1e6, "B": 1e9}

damage_property_parts = data["DAMAGE_PROPERTY"].str.extract(r"^([\d.]+)?([KMB])?$")
# fills any data NaN or Null
populated_data = pandas.to_numeric(damage_property_parts[0], errors="coerce").fillna(1 if damage_property_parts[1].notna().any() else 0)
# Takes populated DAMAGE_PROPERTY using mult map to determine unit for multiplication to standard single dollar
data["DAMAGE_PROPERTY"] = (
    populated_data
    * damage_property_parts[1].map(mult).fillna(1)
)

print(data["DAMAGE_PROPERTY"])
