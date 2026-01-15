from typing import Optional

from airflow.sdk import get_current_context, task, task_group, Asset, Metadata

from lib.domain.events.base import dataset_extra
from lib.domain.download import upload_files
from lib.domain.sources.definitions import Source
from lib.tasks.download import stop_if_already_downloaded


@task_group(group_id="download")
def download_group(
    source: Source,
    output_asset: Asset,
    input_asset: Optional[Asset] = None,
    force_download: bool = False
):
    @task(
        inlets=[input_asset] if input_asset else [],
    )
    def get_version():
        context = get_current_context()
        if input_asset:
            event = context["inlet_events"][input_asset][-1]
            return event.extra["payload"]["latest_version"].strip()

        params_version = context['params'].get('version')
        assert params_version, "version param must be provided if no input asset"
        return params_version.strip()

    @task(outlets=[output_asset])
    def download(version: str):
        dataset_path = upload_files(source, version)
        extra = dataset_extra(source, version=version, dataset_path=dataset_path)
        yield Metadata(output_asset, extra)

    get_version_task = get_version()
    download_task = download(get_version_task)
    (
        get_version_task
        >> stop_if_already_downloaded(source, get_version_task, force_download)
        >> download_task
    )
