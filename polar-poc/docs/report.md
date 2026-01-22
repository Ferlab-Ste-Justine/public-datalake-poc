## Main Questions

- Is the effort required to convert existing Spark jobs to Polars reasonable?
- Is the Polars framework mature and stable enough for production use?
- Can Polars handle very large tables and scale to meet our data processing needs?

## Learning effort

The transition between spark and polars requires some learning, but is easy and intuitive
for spark users.

### Similarities

- Both use chained, SQL-like DataFrame transformations (`select`, `filter`, `groupby`, `agg`)
- Both have a `col` object for building column expressions
- Many functions, aggregations and transformations are similar or directly equivalent
- Both support user-defined function UDFs
- Both support sql interface

### Differences

- **Execution mode**: Spark is always lazy, Polars supports both lazy and eager execution.
- **Architecture**: Spark is designed for cluster/distributed; Polars is pptimized for single-machine, multi-threaded performance
- **Function coverage**: Spark offers more built-in functions, aggregations and windows; Polars covers essentials, but advanced features may require costom code.
- **Edge case handling**: Behaviors can differ for specific edge cases (ex: null values) - review function docs carefully when converting
- **Python integration**: Polars, being native to Python, can integrates more easily with python libraries.  For example, it is already possible to use some numpy functions directly in column expressions. See https://docs.pola.rs/user-guide/expressions/numpy-functions/ . Expect more integrations in the future.


## Conversion effort

- See [conversion_guide.md](conversion_guide.md) for tips and patterns encountered during this POC. 

- See [conversion_effort_analysis.md](conversion_effort_analysis.md)
or a table-by-table breakdown of the conversion effort, including estimated difficulty and any challenging code areas.


## Maturity

Polars is very promising, but lack maturity in comparison to spark.

- Some bugs/issues may arise more frequently and require workarounds.
- More rigorous QA/testing needed, especially early in migration.


### Community feedback

There is some community feedback suggesting that certain basic features in Polars have lacked maturity in the past:
https://news.ycombinator.com/item?id=38921826

Most of these comments are from 2-3 years ago, so the situation has likely improved, but it’s reasonable to expect that some issues may still arise.


### Maturity-related issues observed in POC

**Error tracing in lazy execution mode**

During this POC, we misused `explode` inside `with_columns` (allowed in Spark, not in Polars). This produced the following error:
  `polars.exceptions.ShapeError: zip node received non-equal length inputs`
In lazy execution mode, the error is only link to the final sink_parquet function in the stack trace.  We had trouble to understand and diagnose the problem.

This is a known issue: [Unclear error message in explode() at the Expr level when collecting with the streaming engine](https://github.com/pola-rs/polars/issues/24161)

In eager mode, the error message is directly associated to the offending line, making the issue easier to understand.

This experience suggests that error tracing can be more challenging in lazy execution mode.

**Using pl.all() break streaming behaviour**

We had out of memory error when using pl.all() in groupBy + agg context, even if we were using the streaming engine and lazy execution mode.

There seem to be several bugs where using a specific functionality is causing out of memory problems. Ex:
https://github.com/pola-rs/polars/issues/25180
https://github.com/pola-rs/polars/issues/24698


**Others**

- No free job profiling tool: there is one available, but it is a paid feature
- no iceberg sink yet


## Scalability

**Performance**:
Execution time for the ClinVar job was comparable to Spark—about 1–2 minutes with Polars versus 3 minutes with Spark.

**Scalability Testing Needed**:
Additional tests are required to better understand Polars’ scalability and to estimate the maximum data volume that can be processed efficiently.  There is a GPU mode that could be interesting to test as well:
https://docs.pola.rs/user-guide/lazy/gpu/
It might not be very mature though as it is in beta.

**Streaming Mode Limitations**:
We observed that Polars’ streaming mode is currently fragile. When streaming is not functional, jobs may require significantly more memory, as Polars cannot adapt to available resources as effectively.

**Best Practices**:
To fully benefit from Polars’ performance optimizations, it is important to run jobs in lazy mode. Lazy execution allows Polars to plan and optimize the computation graph before execution.

**Note**:
Polars is designed for high performance by leveraging Rust and efficient use of a single machine’s resources. For more details on Polars optimizations in lazy mode, see this documentation:
https://docs.pola.rs/user-guide/lazy/optimizations/
