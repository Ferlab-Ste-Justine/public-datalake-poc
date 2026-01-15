from airflow.sdk import Asset, AssetWatcher

from lib.assets.detect.clinvar import ClinvarTrigger
from lib.domain.datalake import get_raw_asset_uri, get_normalized_asset_uri
from lib.domain.sources.definitions import Source


clinvar_upstream_version_asset = Asset(
    uri='x-upstream-version-clinvar',
    name="clinvar_upstream_version",
    watchers=[AssetWatcher(name='clinvar_upstream_version_watcher', trigger=ClinvarTrigger())]
)
clinvar_raw_dataset_asset = Asset(
    uri=get_raw_asset_uri(Source.CLINVAR),
    name="clinvar_raw_dataset"
)
clinvar_normalized_dataset_asset = Asset(
    uri=get_normalized_asset_uri(Source.CLINVAR),
    name="clinvar_normalized_dataset"
)
clinvar_published_dataset_asset = Asset(
    uri="x-public-dataset-clinvar",
    name="clinvar_published_dataset"
)


gnomad_v4_cnv_raw_dataset_asset = Asset(
    uri=get_raw_asset_uri(Source.GNOMAD_V4_CNV),
    name="gnomad_v4_cnv_raw_dataset"
)
gnomad_v4_cnv_normalized_dataset_asset = Asset(
    uri=get_normalized_asset_uri(Source.GNOMAD_V4_CNV),
    name="gnomad_v4_cnv_normalized_dataset"
)
gnomad_v4_cnv_published_dataset_asset = Asset(
    uri="x-public-dataset-gnomad-v4-cnv",
    name="gnomad_v4_cnv_published_dataset"
)


example_tar_raw_dataset_asset = Asset(
    uri=get_raw_asset_uri(Source.EXAMPLE_TAR),
    name="example_tar_raw_dataset"
)
example_tar_normalized_dataset_asset = Asset(
    uri=get_normalized_asset_uri(Source.EXAMPLE_TAR),
    name="example_tar_normalized_dataset"
)
example_tar_published_dataset_asset = Asset(
    uri="x-public-dataset-example-tar",
    name="example_tar_published_dataset"
)
