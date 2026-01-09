## Pain Points & Limitations with Airflow Assets

### All Triggers

- Airflow automatically detects new asset triggers (similar to DAGs), but code changes to triggers are not picked up until Airflow is restarted.

- Fragmented documentation: hard to find examples matching chosen syntax (single-task dag created with @asset decorator or with taskflow api). This was the most helpful: https://www.astronomer.io/docs/learn/airflow-datasets

### Event-Based Asset Triggers

- No UI indication when trigger code fails.
    - Workaround: catch exceptions, emit "error event" (DAG must handle).

- Custom trigger needed (did not use `HttpEventTrigger`):
    - Can't add custom event data (only raw base64 response).
    - Response check must be passed as a string (fragile).
    - No error reporting (just logs).

- Docs: Hard to find info on trigger event metadata in consuming DAGs; This was helpful:
 https://airflow.apache.org/docs/apache-airflow-providers-common-messaging/stable/triggers.html

- Extra metadata: format differ from standard asset: accessible via event.extra["payload] instead event.extra. Consuming dags must take this into account

### Standard Asset Scheduling

- Asset uniqueness: only one asset per URI is kept; unclear which.

## No more webserver pod in airflow 3

- `service.type` now under `apiServer` (not `webserver`).
- Still set UI user/pass under `webserver` in values.yaml.


## Airflow docker image

- Used Airflow 3 base image (includes most providers).
- For prod: build custom image, install only needed providers.


## Questions

### Is it a good idea to use assets ? How should we design our dags/assets?

Choosing between traditional task flow and asset-based (messaging) approaches isn’t straightforward—both have pros and cons.

It is a good idea to keep the codebase flexible. This way, we can leverage asset features where they make sense, but also easily pivot to more traditional task flows if needed as the project evolves and as we gain experience with Airflow 3.

Airflow encourage to align asset definitions with resource updates events.
The idea is to be able to visualize the resources and the pipelines that update them in the UI. It is a good idea to adopt clear naming conventions for assets and dags to ease UI filtering.

### What are pros/cons of using assets?

Pros:
- Better visibily on the resources created/updated
- Encourages smaller, decoupled components that are easier to test and maintain.

Cons:
- the data flow is multi-dag and less linear, which can make it harder to track compared to the single-dag sequential approach
- Tend to generate a lot of dags
- Some pitfalls exist, such as:
    - Errors in event-based asset triggers are not always surfaced in the UI.
    - Defining multiple assets with the same name/URI can accidentally break or overwrite data flows.
