from airflow.triggers.base import TriggerEvent

from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry


def dataset_extra(source: Source, version: str, dataset_path: str) -> dict:
    source_id = SourceRegistry.get_source_id(source)
    return {"version": version, "source": source_id, "dataset_path": dataset_path}


def version_change_payload(source: Source, current_version: str, latest_version: str) -> dict:
    source_id = SourceRegistry.get_source_id(source)
    return {"current_version": current_version, "latest_version": latest_version, "source": source_id}


def error_event(error_details: str) -> TriggerEvent:
    """Utility to create a standardized TriggerEvent for errors."""
    return TriggerEvent(payload={
        'error': error_details
    })
