## ETL

`data.py` handles normal transformation functions as well as getting the data from CSV
`property_damage.py` handles parsing property damage from units (1K, 2M, etc.) to singular dollar values (1000, 2000000, etc.) 
`timezone_to_utc.py` handles parsing timezones information to UTC for consistent storage/indexing from local times
`main.py` handles helper functions

## Split

`data.py` contains assing_split which takes in a key and returns whether or not that data is valid training, eval, or test data.

## Versioning

Uses [DVC](https://doc.dvc.org/example-scenarios/versioning-data-and-models) dataset versioning system.

## Orchestration

Uses [Prefect](https://github.com/PrefectHQ/prefect) workflow automation
