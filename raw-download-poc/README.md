# Public Datalake Download POC

## Overview

This repository contains a proof-of-concept (POC) for managing public datalake downloads using Airflow 3’s asset features.


## Goals

- Cleaning up and modularizing download logic originally from the `Qlin` project
- Evaluate the practicality and benefits of Airflow’s asset-based scheduling


## Main Conclusions

**Pros:**
- Asset view: clear version change history; easy to see last update per source and event processing details
- Events reusable by other consumers
- DAG logic more decoupled

**Cons:**
- Trigger error handling not surfaced by Airflow; requires custom event/error logic
- Asset events format is not the same for event-based assets vs regular assets
- If 2 assets are defined with the same uri, airflow will keep only one
- Not always well documented if not using the single-function dag architecture (via @asset annotation)
- Documentation is often fragmented: examples are usually provided for either the @asset annotation or the task-flow API.  It can be difficult to know where to look for examples matching one's chosen approach.


## Code Structure

- `dags/`: Airflow DAG definitions are at the root of this folder
- `dags/lib/assets/`: Code for defining airflow assets.
- `dags/lib/domain/`: Business logic.
- `dags/lib/domain/sources/`: Source definitions (metadata, file specifications)
- `dags/lib/domain/catalog.py`: Stub catalog implementation to retrieve and update current sources versions
- `dags/lib/groups/`: Reusable task groups (@task_group)
- `dags/lib/task/`: airflow tasks (@task)
- `dags/lib/utils/`: Shared utility functions
- `dags/lib/config.py`: Global configuration variables.
- `dags/lib/dag_settings.py`: Global DAG settings


## Differences between POC and qlin code

- Utility functions have been reorganized, with some minor changes to function signatures.
- Version storage logic has been removed, as a different architecture will be used for this in the future.
- Data source configuration classes have been reviewed and extended to cover more scenarios.
- Task outputs avoid passing the entire source configuration; only the necessary information is accessed via SourceRegistry.


## Why this is a POC

- Scope is limited to download and version detection; this is not a full import pipeline.
- Most components are stubs (the download logic itself is functional).
- Only a few sources are implemented; one is a fake source for testing purposes.
- Error notification logic is not implemented.
- No unit tests yet.
- Proper requirements.txt and Docker image setup are still needed.

