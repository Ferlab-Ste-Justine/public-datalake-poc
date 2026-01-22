from datetime import timedelta

from airflow.providers.amazon.aws.operators import ecs


from lib import config
from lib.domain.datalake import get_normalized_datalake_url, get_raw_datalake_url
from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry
from lib.domain.normalize import get_normalize_job_options


# Example structure for Airflow operators that run ECS tasks.
# ----------------------------------------------------------------
# This code has not been executed, so errors may be present.
# It is meant to show how ECS operators could be organized and to highlight
# the AWS resources and configurations that would be required.
#
# The design is inspired by the radiant-portal-pipeline project.
# There may be simpler or more efficient approaches; this is just one possible pattern.
#
# For now, there is only one operator to create the parquet file, but there might be more 
# operators needed to create/commmit the file as an iceberg table


class BaseECSOperator:
    @staticmethod
    def _get_ecs_context():
        return dict(
            cluster=config.ecs_cluster,
            launch_type=config.ecs_launch_type,
            task_definition=config.ecs_task_definition,
            awslogs_group=config.ecs_task_log_group,
            awslogs_region=config.ecs_task_log_region,
            awslogs_stream_prefix=config.ecs_norm_task_log_stream_prefix,
            awslogs_fetch_interval=timedelta(seconds=config.ecs_log_fetch_interval_seconds),
            network_configuration=config.ecs_network_configuration,
            aws_conn_id=config.aws_conn_id
        )


class Normalize(BaseECSOperator):
    @staticmethod
    def get_create_parquet_files(source: Source, version: str):
        source_id = SourceRegistry.get_source_id(source)
        options = get_normalize_job_options(source, version)

        return ecs.EcsRunTaskOperator.partial(
            **dict(
                pool=config.pool_normalization,
                task_id="normalize",
                task_display_name="[ECS] normalize (create parquet file)",
                overrides={
                    "containerOverrides": [
                        {
                            "name": f"{config.ecs_norm_container_name}",
                            "command": [
                                "python",
                                "normalize.py",
                                f"{source_id}"
                            ] + [f"--{key}={value}" for key, value in options.items()]
                        }
                    ]
                },
            )
            | Normalize._get_ecs_context()
        )

