from prefect import flow,task

@task(retries=2)
def ingest(): ...
@task
def normalize_timezones(df): ...
@task
def normalize_money(df): ...
@task
def make_splits(df): ...
@task
def validate(df): ...  # schema checks + leakage assertion

@flow(log_prints=True)
def pipeline():
    df = ingest()
    df = normalize_money(normalize_timezones(df))
    df = make_splits(df)
    validate(df)

if __name__ == "__main__":
    pipeline()
