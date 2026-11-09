from typing import cast

import pandas

from noaa.data import get_data


def parse_property_damage(data: pandas.DataFrame) -> pandas.DataFrame:
    """
    transforms property damage numbers from units to singular dollar value (ex: 1K -> 1000)
    """
    assert data is not FileNotFoundError
    data = cast(pandas.DataFrame, data)

    mult = {"K": 1e3, "M": 1e6, "B": 1e9}

    damage_property_parts = data["DAMAGE_PROPERTY"].str.extract(r"^([\d.]+)?([KMB])?$")
    # fills any data NaN or Null
    populated_data = pandas.to_numeric(
        damage_property_parts[0], errors="coerce"
    ).fillna(1 if damage_property_parts[1].notna().any() else 0)
    # Takes populated DAMAGE_PROPERTY using mult map to determine unit for multiplication to standard single dollar
    data["DAMAGE_PROPERTY"] = populated_data * damage_property_parts[1].map(
        mult
    ).fillna(1)

    return data


print(
    parse_property_damage(
        cast(
            pandas.DataFrame,
            get_data("datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv"),
        )
    )
)
