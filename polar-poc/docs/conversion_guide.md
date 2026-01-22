## Conversion guide

When converting Spark code to Polars, prefer direct equivalents unless there is a good reason to change the logic. Always check the documentation and pay attention to corner cases (e.g., null values, ordering).


### Regex Conversion Tips


- **Regex Replace**
  - **Spark:** `regexp_replace(column, regex, replacement)`  
    - Regex patterns in Spark require double backslashes (`\\`) for escaping.
  - **Polars:** `column.str.replace(regex, replacement)`  
    - In Polars, use a single backslash (`\`) for escaping in regex patterns.

- **Splitting Strings**
  - **Spark:** `split(column, pattern_regex)`  
    - The pattern is always treated as a regex.
  - **Polars:** `column.str.split(by, literal=True)`  
    - By default, `literal=True` means the delimiter is a normal string, i.e. not a regex.


### Accessing dataframe columns can be costly in polars

Accessing columns or schema directly (e.g., `df.columns`, `df.schema` outside of expressions) can trigger a collection operation.

Prefer using polar.all() expression to refer to all columns in a transformation instead.

Note that somehow accessing columns using either direct dataframe attribute or polar.all() seem to break the streaming engine behaviour in our case.


### Avoid using explode in with_columns

The with_columns context expect resulting column definitions to be the same
length as the other columns in the dataframe.

Thus, unlike with spark, one cannot use an explode expression in with_columns statement.
Use the dataframe explode transformation instead.

Incorrect (will fail):
```
new_df = df.with_columns(
    pl.col("tags").explode()  # ❌ Not allowed in with_columns
)
```

Correct:
```
new_df = df.explode("tags")  # ✅ Use explode as a DataFrame transformation
```
