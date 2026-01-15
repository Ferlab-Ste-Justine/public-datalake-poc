from airflow.sdk import get_current_context, task


@task
def get_force_download():
    context = get_current_context()
    param_force_download = context['params'].get('force_download')
    return param_force_download.strip().lower() == 'yes'
