# AWS accounts decision for Public Datalake

* Status: proposed
* Deciders: TODO

Technical Story: [https://d3b.atlassian.net/browse/SJRA-1091](https://d3b.atlassian.net/browse/SJRA-1091)

## Context and Problem Statement

We are building a **public datalake** to share public genomics data with external clients (radiant). The datalake will use AWS Glue as the data catalog and S3 as the underlying storage.  The main ETL components (Airflow and EMR) will also be hosted in AWS.

**Key questions:**
- In which AWS account should we store the data and the catalog?
- Which AWS account should host the ETL (i.e. Airflow + EMR)?

## Decision Drivers

_Note: This section documents resource needs and main factors influencing the account choice. Separate ADRs may be created for access, security, or billing mechanisms._

- **Security and Isolation:**  
  - Only public data will be stored, but to minimize risk and avoid accidental exposure, the datalake should not share an account with sensitive resources.
  - All access must be authenticated and controlled; no anonymous/public S3 access.

- **Environments and Data Organization:**
  - Dedicated AWS resources (buckets, catalog, Airflow, etc.) are needed for QA, staging, and production environments
  - Within each environment, multiple S3 buckets may be required to support a medallion architecture (e.g., raw, processed, curated zones)

- **Access Patterns:**
  - Clients will access data via the AWS Glue catalog (not directly via S3), with read-only permissions managed by Lake Formation.
  - Data will typically be federated/copied into client systems (cross-account or external to AWS).

- **Costs:**
  - S3 storage and data transfer are important cost drivers
  - S3 Requester Pays could be used to shift data transfer costs to clients,  but is **not compatible** with Lake Formation vended credentials
  - EMR compute costs depends on cluster size and duration; cross region data transfer is not free, so resources should ideally be in the same region as the S3 bucket(s).
  - Glue Data Catalog and Lake Formation incur minor metadata and governance costs.
  - Airflow/ETL infrastructure costs are also a consideration.

- **ETL Integration:**
  - The ETL pipeline (Airflow / EMR) may run in the same or a separate AWS account.
  - ETL needs access to both Glue catalog and S3 (some raw data may not be cataloged).
  - Sharing infrastructure (e.g., Airflow) between the public datalake and other workloads may help minimize costs.

- **Airflow Version Considerations:**
  - There is an intention to share Airflow infrastructure with another application currently using Airflow 2, which would reduce costs and ease immediate integration.
  - Choosing Airflow 3 may involve more initial setup and higher costs until the other application is migrated, but avoids future migration for the public datalake and enables use of recent features from the start.
 
## Considered Options

_TODO: To be completed collaboratively. Options may include:_
- Hosting all resources in a dedicated public datalake account
- Splitting ETL and storage/catalog across accounts
- Sharing Airflow with other workloads/applications

## Decision Outcome

_TODO: To be finalized with input from all stakeholders. The outcome should specify:_
- Chosen account(s) for storage (S3 and Glue)
- Chosen account(s) for ETL (Airflow and EMR)
- Any resources that will be shared with other workloads

## Links

- [lake formation](https://docs.aws.amazon.com/lake-formation/latest/dg/how-it-works.html)
- [lake formation vended credentials not compatible with requester pay](https://docs.aws.amazon.com/lake-formation/latest/dg/register-location.html)
- [s3 data transfer pricing](https://aws.amazon.com/s3/pricing/)
- [Apache Airflow® 3 is Generally Available!](https://airflow.apache.org/blog/airflow-three-point-oh-is-here/)