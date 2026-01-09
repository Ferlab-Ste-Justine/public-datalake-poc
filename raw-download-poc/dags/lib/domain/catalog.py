from airflow.sdk import Variable

from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry

# Stub implementation: Airflow Variables are used here as a temporary solution for state management.


async def get_current_version(source: Source) -> str | None:
    """Retrieve the current version for a given source."""
    source_id = SourceRegistry.get_source_id(source)
    return Variable.get(key=f"{source_id}_current_version", default=None)


async def set_current_version(source: Source, version: str):
    """Set the current version for a given source."""
    source_id = SourceRegistry.get_source_id(source)
    Variable.set(key=f"{source_id}_current_version", value=version)
