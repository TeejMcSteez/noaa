from noaa.data import get_bulk_data


data = get_bulk_data("gs://noaa-ncei-ipg/notebooks/data/stormevents/storm_events_database_details/*/*.parquet")

data.to_csv("datasets/google")
