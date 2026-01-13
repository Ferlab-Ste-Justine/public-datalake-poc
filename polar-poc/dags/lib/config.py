from airflow.sdk import Variable

environment = Variable.get('env', 'dev')

pool_normalization = "normalization"
compute_environment = "k8s"

aws_conn_id = "pbdl_aws"

raw_bucket_name = f"pbdl-{environment}-raw"
raw_datalake_prefix_template = '{{SOURCE}}/{{VERSION}}'
norm_bucket_name = f"pbdl-{environment}-norm"
norm_datalake_prefix_template = '{{SOURCE}}/{{VERSION}}'

# ECS setup
# requires: aws connection
# the following resources must be pre-created (terraform):
#  - ECS Cluster
#  - ECS Task Definition
#  - CloudWatch Log Group
ecs_log_fetch_interval_seconds = 5
ecs_cluster = "pbdl-ecs-cluster"
ecs_task_definition = "pbdl-ecs-task-def"
ecs_launch_type = "FARGATE"
ecs_network_configuration = {} # ???
ecs_task_log_group = f"/ecs/pbdl/{environment}"
ecs_task_log_region = "ca-central-1"
ecs_norm_task_log_stream_prefix = "normalization"
ecs_norm_container_name = "pbdl-ecs-normalization-container"
ecs_commit_partitions_container_name = "pbdl-ecs-commit-partitions-container"

# Kubernetes setup (FOR THIS POC ONLY)
k8s_namespace = f"pubdlk"
k8s_norm_image = "public-datalake-normalization:latest"
