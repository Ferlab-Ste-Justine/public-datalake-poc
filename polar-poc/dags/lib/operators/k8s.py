import os

from airflow.sdk import task

from lib import config
from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry
from lib.domain.normalize import get_normalize_job_options


class BaseK8SOperator:
    @staticmethod
    def _get_k8s_context():
        return dict(
            namespace=config.k8s_namespace,
            image=config.k8s_norm_image,
            image_pull_policy="IfNotPresent",
            get_logs=True,
            is_delete_operator_pod=True,
            env_vars={ # TODO use secrets instead to avoid leaking credentials in pod specs
                "AWS_REGION": os.getenv("AWS_REGION"),
                "AWS_ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
                "AWS_SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
                "AWS_ENDPOINT_URL": os.getenv("AWS_ENDPOINT_URL"),
            }
        )


class Normalize(BaseK8SOperator):
    @staticmethod
    def get_create_parquet_files(source: Source, version: str):
        @task.kubernetes_cmd(
            **dict(
                pool=config.pool_normalization,
                task_id="normalize",
                task_display_name="[K8s] Normalize (Create Parquet Files)",
                name="normalize",
                do_xcom_push=True,
            )
            | Normalize._get_k8s_context()
        )
        def normalize(source: Source, version: str) -> list[str]:
            options = get_normalize_job_options(source, version)
            job_id = SourceRegistry.get_source_id(source)
            return [
                "python",
                "normalize.py",
                job_id,
            ] + [f"--{key}={value}" for key, value in options.items()]

        return normalize(source=source, version=version)
