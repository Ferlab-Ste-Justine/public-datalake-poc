## POC Description

1. Implemented ClinVar normalization logic using Polars and executed it via Airflow. Use lazy execution and streaming engine.
2. Documented encountered issues and learnings (see [docs/report.md](docs/report.md)).
3. Analyzed conversion effort for migrating Spark normalization jobs to Polars, with a difficulty estimate for each table (easy/medium/hard).

Notes:
- Airflow orchestration was implemented using the KubernetesPodOperator.
- Attempted to set up AWS ECS locally with LocalStack, but ECS support is paid-only.  
  ECS-related code components are included in the POC (see `operators/ecs`) and ready for future testing in an AWS environment.


The choice of the VCF library may require further evaluation and experimentation. See details below.


## VCF library

Using [polars-bio](https://github.com/biodatageeks/polars-bio) for now.
- It is natively compatible with Polars DataFrames and supports both lazy execution and streaming, which are essential for handling large genomic datasets efficiently
- It supports many other data formats in addition to vcf
- Seems actively maintained (recent commits)
- A few hundreds of stars on the repo, which is not bad for a bioinfo repo

Gotchas:
- Does not support reading per-sample metrics from VCF files. If this becomes necessary, we’ll need to consider other solutions
- the docker image becomes quite large (2-3 Gb) and takes about 20 minute to build due to the lack of pre-built wheel.  This could likely be optimized with further investigation.

Other options considered:
- biobear: appears unmaintained (broken documentation link, no commits in over a year)
- vcformer: not easily installable (only available via github master branch)
- alternative approach: it is possible to use a native python VCF parser to load the data into an array or PyArrow dataframe and then convert to polars dataframe.  This approach might not support polars lazy execution or streaming features out of the box, however.


## To execute the demo

For the minikube setup, follow the instructions in [sandbox/README.md](sandbox/README.md).

Alternatively, you can execute in a venv:
```
# create python environment
python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install polars polars-bio

# download clinvar data
mkdir data
curl -o data/clinvar.vcf.gz https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz 

# execute the clinvar normalization script
EXPORT PYTHON_PATH=src
python scripts/normalize.py clinvar --input_path=data/clinvar.vcf.gz --output_path=output/norm_clinvar.parquet 
```


## Why this is a POC

- Additional tests are needed to confirm that the final ClinVar schema matches the expected output.
- Sampling is currently used to avoid out-of-memory errors when running in Minikube, as streaming mode is not fully functional.
- The polars python code structure does not follow Ferlab’s standard organization.
- Airflow orchestration is set up for Kubernetes; in production, we plan to run jobs on AWS instead.
- The docker image takes 20 minutes to build and is quite big (about 2 Gig).


## Citations

(Requested by polars-bio)

@article{10.1093/bioinformatics/btaf640,
    author = {Wiewiórka, Marek and Khamutou, Pavel and Zbysiński, Marek and Gambin, Tomasz},
    title = {polars-bio—fast, scalable and out-of-core operations on large genomic interval datasets},
    journal = {Bioinformatics},
    pages = {btaf640},
    year = {2025},
    month = {12},
    abstract = {Genomic studies very often rely on computationally intensive analyses of relationships between features, which are typically represented as intervals along a one-dimensional coordinate system (such as positions on a chromosome). In this context, the Python programming language is extensively used for manipulating and analyzing data stored in a tabular form of rows and columns, called a DataFrame. Pandas is the most widely used Python DataFrame package and has been criticized for inefficiencies and scalability issues, which its modern alternative—Polars—aims to address with a native backend written in the Rust programming language.polars-bio is a Python library that enables fast, parallel and out-of-core operations on large genomic interval datasets. Its main components are implemented in Rust, using the Apache DataFusion query engine and Apache Arrow for efficient data representation. It is compatible with Polars and Pandas DataFrame formats. In a real-world comparison (107 vs. 1.2×106 intervals), our library runs overlap queries 6.5x, nearest queries 15.5x, count\_overlaps queries 38x, and coverage queries 15x faster than Bioframe. On equally-sized synthetic sets (107 vs. 107), the corresponding speedups are 1.6x, 5.5x, 6x, and 6x. In streaming mode, on real and synthetic interval pairs, our implementation uses 90x and 15x less memory for overlap, 4.5x and 6.5x less for nearest, 60x and 12x less for count\_overlaps, and 34x and 7x less for coverage than Bioframe. Multi-threaded benchmarks show good scalability characteristics. To the best of our knowledge, polars-bio is the most efficient single-node library for genomic interval DataFrames in Python.polars-bio is an open-source Python package distributed under the Apache License available for major platforms, including Linux, macOS, and Windows in the PyPI registry. The online documentation is https://biodatageeks.org/polars-bio/ and the source code is available on GitHub: https://github.com/biodatageeks/polars-bio and Zenodo: https://doi.org/10.5281/zenodo.16374290. Supplementary Materials are available at Bioinformatics online.},
    issn = {1367-4811},
    doi = {10.1093/bioinformatics/btaf640},
    url = {https://doi.org/10.1093/bioinformatics/btaf640},
    eprint = {https://academic.oup.com/bioinformatics/advance-article-pdf/doi/10.1093/bioinformatics/btaf640/65667510/btaf640.pdf},
}