
from airflow.sdk import task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from lib.config import raw_connection_id, raw_bucket_name
from lib.domain.sources.definitions import Source
from lib.domain.datalake import get_raw_datalake_prefix

s3 = S3Hook(raw_connection_id)


@task.short_circuit(ignore_downstream_trigger_rules=True)
def stop_if_already_downloaded(source: Source, version: str, force_download: bool = False) -> str:
    if force_download:
        return True

    return not s3.check_for_prefix(
        prefix=get_raw_datalake_prefix(source, version),
        delimiter="/",
        bucket_name=raw_bucket_name
    )
