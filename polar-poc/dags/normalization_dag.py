from airflow.sdk import dag

from lib.operators import ecs, k8s

from lib import config
from lib.domain.sources.definitions import Source


@dag(
    dag_id="polar-poc-normalization-dag",
    schedule=None,
    start_date=None,
    catchup=False,
    tags=["polar", "normalization"],
)
def normalization_dag():
    # TODO: express as a parameter instead of hardcoding
    source = Source.CLINVAR
    version = "foo"

    normalization_operator = ecs.Normalize.get_create_parquet_files(source, version) if config.compute_environment == "ecs" else k8s.Normalize.get_create_parquet_files(source, version)
    
    normalization_operator
    

normalization_dag()