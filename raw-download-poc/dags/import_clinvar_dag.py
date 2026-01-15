
import datetime

from airflow.decorators import dag
from airflow.sdk import Param

from lib import dag_settings
from lib.assets.definitions import clinvar_upstream_version_asset, clinvar_raw_dataset_asset, clinvar_normalized_dataset_asset, clinvar_published_dataset_asset
from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry
from lib.groups.download import download_group
from lib.groups.normalize import normalize_group
from lib.groups.publish import publish_group
from lib.tasks.params import get_force_download


clinvar_dag_settings = {
    "tags": [SourceRegistry.get_source_id(Source.CLINVAR)],
    "default_args": dag_settings.default_args,
    "start_date": datetime.datetime(2026, 1, 1),
}


@dag(
    schedule=clinvar_upstream_version_asset,
    params={
        'force_download': Param('no', enum=['yes', 'no']),
        'version': Param('', type=['null', 'string']),
    },
    **clinvar_dag_settings
)
def clinvar_download():
    force_download_task = get_force_download()
    download_tasks = download_group(
        source=Source.CLINVAR,
        output_asset=clinvar_raw_dataset_asset,
        input_asset=clinvar_upstream_version_asset,
        force_download=force_download_task
    )
    force_download_task >> download_tasks


@dag(schedule=clinvar_raw_dataset_asset, **clinvar_dag_settings)
def clinvar_normalize():
    normalize_group(
        source=Source.CLINVAR,
        output_asset=clinvar_normalized_dataset_asset,
        input_asset=clinvar_raw_dataset_asset
    )


@dag(schedule=clinvar_normalized_dataset_asset, **clinvar_dag_settings)
def clinvar_publish():
    publish_group(
        source=Source.CLINVAR,
        output_asset=clinvar_published_dataset_asset,
        input_asset=clinvar_normalized_dataset_asset
    )


clinvar_download()
clinvar_normalize()
clinvar_publish()
