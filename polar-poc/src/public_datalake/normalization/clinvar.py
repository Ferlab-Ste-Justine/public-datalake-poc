# TODOs
# - we might want to convert list types to array types (polars has both)
# - compare with spark normalized clinvar schema and values

# Things to verify in original spark code
# - We drop a column that no longer exits? clin_sig_original?
# - Weird use of concat_ws, I think this function is not supposed to be used on a single list column, but rather on multiple string columns ...


import polars as pl
from polars import LazyFrame
from polars import col
import polars_bio as pb


def extract(raw_input_path) -> LazyFrame :
    return pb.scan_vcf(raw_input_path)


def transform(input_df: LazyFrame) -> LazyFrame:

    intermediate_df = (
        input_df
        .gather_every(1000)  #TODO: to avoid out of memory issues, should be removed for production
        .select(pl.all().name.to_lowercase())
        .rename(
            {
                "chrom": "chromosome", 
                "alt":"alternate", 
                "ref":"reference", 
                "start": "start", 
                "end": "end",
                "clnsig": "clin_sig",
                "clnsigconf": "clin_sig_conflict"
            }
        )
        .with_columns(
            clin_sig=col("clin_sig")
                .list.join("|")
                .str.replace(r"^_|\|_|/", "|")
                .str.split("|"),
            clnrevstat=col("clnrevstat")
                .list.join("|")
                .str.replace(r"^_|\|_|/", "|")
                .str.split("|"),
            clin_sig_conflict=col("clin_sig_conflict")
                .list.join("|")
                .str.replace(r"\(\d{1,2}\)","")
                .str.split("|")
        )
    )

    return (_with_interpretations(intermediate_df)
        .with_columns(
            clndisdb=col("clndisdb")
                .list.join("|")
                .str.split("|"),
            clndn=col("clndn")
                .list.join("")
                .str.split("|")
        )
        .with_columns(
            conditions=col("clndn")
                .list.join("|")
                .str.replace("_", "")
                .str.split("|"),
            clndisdbincl=col("clndisdbincl")
                .list.join("")
                .str.split("|")
            ,
            clndnincl=col("clndnincl")
                .list.join("")
                .str.split("|"),
            mc=col("mc")
                .list.join("|")
                .str.split("|"),
            inheritance=col("origin").map_elements(_inheritance_udf, return_dtype=pl.List(pl.String))
        )
        .drop("clndn")
        # The original statement was this, but it does not work because clin_sig_original don't exist
        #.drop("clin_sig_original", "clndn")
    )


def load(output_df: LazyFrame, output_path: str) -> None:
    #print(output_df.schema)
    output_df.sink_parquet(path=output_path, mkdir=True)


def _with_interpretations(input_df: LazyFrame) -> LazyFrame:
    fields_to_remove = ["chromosome", "start", "end", "reference", "alternate", "interpretation"]
    
    return (
        input_df
            .with_columns(interpretation=col("clin_sig").list.set_union(col("clin_sig_conflict")).list.filter(pl.element() != ""))
            .explode(col("interpretation"))
            .group_by("chromosome", "start", "end", "reference", "alternate")
            .agg(
                pl.all().exclude(fields_to_remove).first(),
                col("interpretation"),
            )
            .with_columns(
                interpretations=col("interpretation").list.unique()
            )
    )


def _inheritance_udf(origin_array: list[str]) -> list[str]:
    unknown = "unknown"
    labels = {
        0:  unknown,
        1: "germline",
        2: "somatic",
        4: "inherited",
        8: "paternal",
        16: "maternal",
        32: "de-novo",
        64: "biparental",
        128: "uniparental",
        256: "not-tested",
        512: "tested-inconclusive",
        1073741824: "other"
    }
    if origin_array is None: #TODO null? Non? empty?
        return [unknown] # mutable.WrappedArray.make(Array(unknown))

    result = []
    for number in origin_array:
        n= int(number)
        if n == 0:
            result.append(unknown)
        else:
            for digit, label in labels.items():
                if digit != 0 and (n & digit) !=0:
                    result.append(label)
    return list(set(result))


def run(input_path: str, output_path: str) -> None:
    raw_df = extract(input_path)
    norm_df = transform(raw_df)
    load(norm_df, output_path)
