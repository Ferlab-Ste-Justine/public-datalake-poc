from airflow.utils.trigger_rule import TriggerRule

# group common dag settings here for now, but I may adjust the approach.
# Note: the on_failure_callback for Slack notifications is missing
default_args = {
    'trigger_rule': TriggerRule.NONE_FAILED
}
