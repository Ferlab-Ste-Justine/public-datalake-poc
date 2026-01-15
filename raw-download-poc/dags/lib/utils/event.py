from airflow.sdk import Asset


def get_event_extra(context: dict, input_asset: Asset) -> dict:
    event = context["inlet_events"][input_asset][-1]
    return event.extra
