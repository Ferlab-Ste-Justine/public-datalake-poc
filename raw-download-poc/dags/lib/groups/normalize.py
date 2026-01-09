
from airflow.sdk import asset, get_current_context, task, task_group, Metadata

from lib.domain.events.base import dataset_extra
from lib.domain.sources.definitions import Source
from lib.domain.normalize import normalize as normalize_fn
from lib.utils.event import get_event_extra


@task_group(group_id="normalize")
def normalize_group(
    source: Source,
    output_asset: asset,
    input_asset: asset
):
    @task(inlets=[input_asset], multiple_outputs=True)
    def parse_event():
        return get_event_extra(get_current_context(), input_asset)

    @task(outlets=[output_asset])
    def normalize(version: str, input_dataset_path: str):
        output_dataset_path = normalize_fn(source, version, input_dataset_path)
        extra = dataset_extra(source, version, output_dataset_path)
        yield Metadata(output_asset, extra)

    parse_event_task = parse_event()
    normalize_task = normalize(parse_event_task["version"], parse_event_task["dataset_path"])

    parse_event_task >> normalize_task
