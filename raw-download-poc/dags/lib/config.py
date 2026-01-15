from airflow.sdk import Variable

environment = Variable.get('env', 'dev')

raw_bucket_name = f"pbdl-{environment}-raw"
raw_datalake_prefix_template = '{{SOURCE}}/{{VERSION}}'
raw_connection_id = 'raw_minio'

norm_bucket_name = f"pbdl-{environment}-normalized"
norm_datalake_prefix_template = '{{SOURCE}}/{{VERSION}}'
