import asyncio

from lib.domain.catalog import set_current_version
from lib.domain.events.base import dataset_extra
from lib.domain.sources.definitions import Source


def publish(source: Source, version: str, dataset_path: str) -> dict:
    """Stub implementation of publish task."""
    # put extra publish logic here ...
    asyncio.run(set_current_version(source, version))
    return dataset_extra(source, version=version, dataset_path=dataset_path)
