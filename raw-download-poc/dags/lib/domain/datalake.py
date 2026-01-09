
from lib.config import raw_bucket_name,  norm_bucket_name, raw_datalake_prefix_template, norm_datalake_prefix_template
from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry


def get_raw_datalake_prefix(source: Source, version: str) -> str:
    source_id = SourceRegistry.get_source_id(source)
    return raw_datalake_prefix_template.replace('{{SOURCE}}', source_id).replace('{{VERSION}}', version)


def get_normalized_datalake_prefix(source: Source, version: str) -> str:
    source_id = SourceRegistry.get_source_id(source)
    return norm_datalake_prefix_template.replace('{{SOURCE}}', source_id).replace('{{VERSION}}', version)


def get_raw_asset_uri(source: Source) -> str:
    prefix = get_raw_datalake_prefix(source, "")
    return f"s3://{raw_bucket_name}/{prefix}"


def get_normalized_asset_uri(source: Source) -> str:
    prefix = get_normalized_datalake_prefix(source, "")
    return f"s3://{norm_bucket_name}/{prefix}"
