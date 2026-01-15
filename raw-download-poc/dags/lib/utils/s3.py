from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import logging
from lib.utils.md5 import compute_file_md5

def get_first_s3_multipart_upload_id(s3: S3Hook, s3_bucket:str, s3_key: str) -> str | None:
    """
    Returns the UploadId of the first active multipart upload for the given S3 key, or None if none exists.
    """
    s3_client = s3.get_conn()
    response = s3_client.list_multipart_uploads(Bucket=s3_bucket, Prefix=s3_key)
    uploads = response.get('Uploads', [])
    upload_id = [upload['UploadId'] for upload in uploads]
    return upload_id[0] if upload_id else None


def bytes_to_human_readable(byteSize: int) -> str:
    mbBytes = byteSize / (1024 * 1024)
    if(mbBytes > 1000):
        gbBytes = mbBytes / 1024
        return f"{gbBytes:.2f} GB"
    return f"{mbBytes:.2f} MB"


def load_file(s3: S3Hook, s3_bucket:str, dest_s3_key:str, local_file_name: str, save_md5 = False):
    s3.load_file(local_file_name, dest_s3_key, s3_bucket, replace=True)
    logging.info(f'file ({local_file_name}) successfully loaded.')

    if save_md5:
        md5 = compute_file_md5(local_file_name)
        s3.load_string(md5, f'{dest_s3_key}.md5', s3_bucket, replace=True)
        logging.info(f'file ({local_file_name}.md5) successfully loaded.')