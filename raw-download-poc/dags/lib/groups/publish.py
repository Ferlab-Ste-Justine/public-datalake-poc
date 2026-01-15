
from airflow.sdk import asset, get_current_context, task, task_group, Metadata

from lib.domain.sources.definitions import Source
from lib.domain.publish import publish as publish_fn
from lib.utils.event import get_event_extra
from lib.tasks.validation import validate


@task_group(group_id="publish")
def publish_group(
    source: Source,
    output_asset: asset,
    input_asset: asset
):
    @task(inlets=[input_asset], multiple_outputs=True)
    def parse_event():
        return get_event_extra(get_current_context(), input_asset)

    @task(outlets=[output_asset], inlets=[input_asset])
    def publish(version: str, dataset_path: str):
        extra = publish_fn(source, version, dataset_path)
        yield Metadata(output_asset, extra)

    parse_event_task = parse_event()
    validate_task = validate(source, parse_event_task["version"], parse_event_task["dataset_path"])
    publish_task = publish(parse_event_task["version"], parse_event_task["dataset_path"])

    parse_event_task >> validate_task >> publish_task
