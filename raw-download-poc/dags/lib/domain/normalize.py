from lib.domain.datalake import get_normalized_datalake_prefix
from lib.domain.sources.definitions import Source


def normalize(source: Source, version: str, input_dataset_path: str) -> str:
    """Stub normalize function"""
    return get_normalized_datalake_prefix(source, version)
