import pandas

data = pandas.read_csv("../../datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv")


mult = {"K": 1e3, "M": 1e6, "B": 1e9}

parts = data["DAMAGE_PROPERTY"].str.extract(r"^([\d.]+)?([KMB])?$")
# fills any data NaN or Null
populated_data = pandas.to_numeric(parts[0], errors="coerce").fillna(1 if parts[1].notna().any() else 0)
# Takes populated DAMAGE_PROPERTY using mult map to determine unit for multiplication to standard single dollar
data["DAMAGE_PROPERTY"] = (
    populated_data
    * parts[1].map(mult).fillna(1)
)

print(data["DAMAGE_PROPERTY"])
