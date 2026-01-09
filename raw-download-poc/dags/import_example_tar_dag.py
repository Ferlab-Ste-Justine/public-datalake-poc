
import datetime

from airflow.sdk import dag, Param

from lib import dag_settings
from lib.assets.definitions import example_tar_raw_dataset_asset, example_tar_normalized_dataset_asset, example_tar_published_dataset_asset
from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry
from lib.groups.download import download_group
from lib.groups.normalize import normalize_group
from lib.groups.publish import publish_group
from lib.tasks.params import get_force_download


example_tar_dag_settings = {
    "tags": [SourceRegistry.get_source_id(Source.EXAMPLE_TAR)],
    "default_args": dag_settings.default_args,
    "start_date": datetime.datetime(2026, 1, 1),
}


@dag(
    schedule=None,
    params={
        'force_download': Param('no', enum=['yes', 'no']),
        'version': Param('some_version', type=['null', 'string']),
    },
    **example_tar_dag_settings
)
def example_tar_download():
    force_download_task = get_force_download()
    download_tasks = download_group(
        source=Source.EXAMPLE_TAR,
        output_asset=example_tar_raw_dataset_asset,
        input_asset=None,
        force_download=force_download_task
    )
    force_download_task >> download_tasks


@dag(schedule=example_tar_raw_dataset_asset, **example_tar_dag_settings)
def example_tar_normalize():
    normalize_group(
        source=Source.EXAMPLE_TAR,
        output_asset=example_tar_normalized_dataset_asset,
        input_asset=example_tar_raw_dataset_asset
    )


@dag(schedule=example_tar_normalized_dataset_asset, **example_tar_dag_settings)
def example_tar_publish():
    publish_group(
        source=Source.EXAMPLE_TAR,
        output_asset=example_tar_published_dataset_asset,
        input_asset=example_tar_normalized_dataset_asset
    )


example_tar_download()
example_tar_normalize()
example_tar_publish()
