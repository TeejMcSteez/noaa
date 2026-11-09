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

    damage_property_parts = cast(
        pandas.DataFrame,
        data["DAMAGE_PROPERTY"].str.extract(r"^(?P<num>[\d.]+)?(?P<unit>[KMB])?$", expand=True),
    )
    num = cast(pandas.Series, damage_property_parts["num"])
    unit = cast(pandas.Series, damage_property_parts["unit"])
    # fills NaN numbers: unit-only values (ex: "K") -> 1, fully empty -> 0
    populated_data = cast(
        pandas.Series,
        pandas.to_numeric(num, errors="coerce"),
    ).fillna(unit.notna().astype(int))
    # Takes populated DAMAGE_PROPERTY using mult map to determine unit for multiplication to standard single dollar
    data["DAMAGE_PROPERTY"] = populated_data * unit.map(mult).fillna(1)

    return data

data = cast(
    pandas.DataFrame,
    get_data("datasets/StormEvents_details-ftp_v1.0_d1950_c20260323.csv"),
)

print(
    parse_property_damage(
        data
    )["DAMAGE_PROPERTY"]
)
