
Below a list of data source names and associated difficulty to convert to polars.


| Source Name  | Difficulty | Justification | Datalake lib components |
|------------- |------------|---------------| ----------------------- |
| 1000_genomes | easy | simple select statement | normalized.OneThousandGenomes |
| hpo_gene_panel | easy | few columns, renaming only | normalized.HPOGeneSet |
| ddd_gene_panel | easy | few columns, renaming + mild normalizations | normalized.DDDGeneSet |
| dbsnp | easy | few columns, custom logic for chromosome renaming, otherwise mild normalization | normalized.DBSNP.scala |
| gnomad | medium | easy normalization, but several tables and somes are large | normalized.gnomad.* (V3, V4, V4 CNV) |
| gnomad_constraint | medium | easy normalization but many columns | normalized.gnomad.GnomadConstraint |
| omim_gene_panel | medium | custom logic for parsing phenotypes | normalized.omim.OmimGeneSet |
| orphanet_gene_panel | medium | custom logic to parse XML and joins | normalized.orphanet.OrphanetGeneSet |
| cosmic_gene_panel | medium | custom udf + folding logic | normalized.cosmic.CosmicGeneSet | 
| ensembl_gene | hard | multiple sources and extra enrich step| normalized.EnsemblMapping + enriched.Genes |
| clinvar | hard | delicate regex-based normalizations, custom udf / grouping logic, many columns | normalized.Clinvvar |
| dbsnfp | hard | many columns and extra enrich step | normalized.DBSNFPRaw, enriched.DBSNFP |
| spliceai | hard | extra enrich step, big volume of data | normalized.SpliceAi, enriched.SpliceAi |

Unknown (datalake lib components not identified yet): ensembl_exon_by_gene, mondo_term
