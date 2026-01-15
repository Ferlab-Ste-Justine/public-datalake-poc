from enum import Enum
from datetime import timedelta

from lib.domain.sources.model import DownloadConfig, FileSpec, SourceMeta

class Source(Enum):
    CLINVAR = "clinvar"
    GNOMAD_V4_CNV = "gnomad_v4_cnv"
    EXAMPLE_TAR = "example_tar" # fake source for testing tar extraction


SOURCES_META = {
    Source.CLINVAR: SourceMeta(
        short_name='clinvar',
        display_name='NCBI Clinvar',
        website='https://www.ncbi.nlm.nih.gov/clinvar/',

        download_config=DownloadConfig(
            poll_interval=timedelta(days=1),
            files=[
                FileSpec(
                    url='https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz',
                    md5_present=True
                )
            ]
        )
    ),
    Source.GNOMAD_V4_CNV: SourceMeta(
        short_name='gnomad_v4_cnv',
        display_name='gnomAD v4 CNV',
        website="https://gnomad.broadinstitute.org/",

        download_config=DownloadConfig(
            poll_interval=None,
            files=[
                FileSpec(
                    url='https://gnomad-public-us-east-1.s3.amazonaws.com/release/4.1/exome_cnv/gnomad.v4.1.cnv.all.vcf.gz',
                    streaming=True
                )
            ]
        )
    ),
    Source.EXAMPLE_TAR: SourceMeta(
        short_name='example_tar',
        display_name='Example with tar extract (fake source)',
        website='https://hgdownload.gi.ucsc.edu/goldenPath/mm10',

        download_config=DownloadConfig(
            poll_interval=None,
            files=[
                FileSpec(
                    url='https://hgdownload.gi.ucsc.edu/goldenPath/mm10/bigZips/p6/mm10.p6.chromOut.tar.gz',
                    extract_members=['2/chr2.fa.out', '3/chr3.fa.out'],
                    md5_present=False
                )
            ]
        )
    )
}
