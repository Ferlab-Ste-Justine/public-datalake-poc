
import datetime

from airflow.sdk import dag, Param

from lib import dag_settings
from lib.assets.definitions import gnomad_v4_cnv_raw_dataset_asset, gnomad_v4_cnv_normalized_dataset_asset, gnomad_v4_cnv_published_dataset_asset
from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry
from lib.groups.download import download_group
from lib.groups.normalize import normalize_group
from lib.groups.publish import publish_group
from lib.tasks.params import get_force_download


gnomad_v4_cnv_dag_settings = {
    "tags": [SourceRegistry.get_source_id(Source.GNOMAD_V4_CNV)],
    "default_args": dag_settings.default_args,
    "start_date": datetime.datetime(2026, 1, 1),
}


@dag(
    schedule=None,
    params={
        'force_download': Param('no', enum=['yes', 'no']),
        'version': Param('4.1', type=['null', 'string']),
    },
    **gnomad_v4_cnv_dag_settings
)
def gnomad_v4_cnv_download():
    force_download_task = get_force_download()
    download_tasks = download_group(
        source=Source.GNOMAD_V4_CNV,
        output_asset=gnomad_v4_cnv_raw_dataset_asset,
        input_asset=None,
        force_download=force_download_task
    )
    force_download_task >> download_tasks


@dag(schedule=gnomad_v4_cnv_raw_dataset_asset, **gnomad_v4_cnv_dag_settings)
def gnomad_v4_cnv_normalize():
    normalize_group(
        source=Source.GNOMAD_V4_CNV,
        output_asset=gnomad_v4_cnv_normalized_dataset_asset,
        input_asset=gnomad_v4_cnv_raw_dataset_asset
    )


@dag(schedule=gnomad_v4_cnv_normalized_dataset_asset, **gnomad_v4_cnv_dag_settings)
def gnomad_v4_cnv_publish():
    publish_group(
        source=Source.GNOMAD_V4_CNV,
        output_asset=gnomad_v4_cnv_published_dataset_asset,
        input_asset=gnomad_v4_cnv_normalized_dataset_asset
    )


gnomad_v4_cnv_download()
gnomad_v4_cnv_normalize()
gnomad_v4_cnv_publish()
