
from lib.domain.sources.definitions import Source
from lib.domain.datalake import get_raw_datalake_url, get_normalized_datalake_url


def get_clinvar_normalize_job_options(input_dir, output_dir) -> dict:
    return {"input_path": input_dir + "/clinvar.vcf.gz", "output_path": output_dir + "/clinvar.parquet"}


def get_normalize_job_options(source: Source, version: str) -> dict:
    input_folder = get_raw_datalake_url(source, version)
    output_folder = get_normalized_datalake_url(source, version)

    if source == Source.CLINVAR:
        return get_clinvar_normalize_job_options(input_folder, output_folder)
    else:
        raise ValueError(f"No normalize job options found for source: {source}")