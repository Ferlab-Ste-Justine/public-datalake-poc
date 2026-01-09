
from airflow.sdk import task
from lib.domain.sources.definitions import Source


@task
def validate(source: Source, version: str, dataset_path: str) -> None:
    """Stub validation function, should raise an exception if validation fails"""
    pass
