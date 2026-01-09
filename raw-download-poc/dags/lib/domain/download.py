from typing import Any
import logging
import tarfile

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import requests

from lib.config import raw_connection_id, raw_bucket_name
from lib.domain.sources.definitions import Source
from lib.domain.sources.model import FileSpec
from lib.domain.sources.registry import SourceRegistry
from lib.domain.datalake import get_raw_datalake_prefix
from lib.utils.md5 import download_and_parse_md5_file, download_and_check_md5
from lib.utils.s3 import get_first_s3_multipart_upload_id, bytes_to_human_readable, load_file

s3 = S3Hook(raw_connection_id)


def upload_files(
        source: Source,
        version: str
):
    dest_s3_prefix = get_raw_datalake_prefix(source, version)
    download_config = SourceRegistry.get_download_config(source)
    for file_spec in download_config.files:
        upload_file(dest_s3_prefix, file_spec)
    return dest_s3_prefix


def upload_file(dest_s3_prefix: str, file_spec: FileSpec):
    download_url = file_spec.get_url()
    dest_file_name = file_spec.name if file_spec.name else download_url.split('/')[-1]
    dest_s3_key = f'{dest_s3_prefix}/{dest_file_name}'
    md5_url = file_spec.get_md5_url()
    md5_hash = download_and_parse_md5_file(md5_url)['hash'] if md5_url else None

    # Note: tar extract is not supported in streaming mode
    if file_spec.streaming:
        stream_upload_or_resume_to_s3(dest_s3_key, download_url, headers=file_spec.headers, md5=md5_hash)

    else:
        logging.info(f'Start upload of {download_url}')
        download_and_check_md5(download_url, dest_file_name, expected_md5=md5_hash)
        if file_spec.tar_extract:
            extract_and_upload_tar_members(
                dest_s3_prefix=dest_s3_prefix,
                member_names=file_spec.extract_members,
                tar_file_name=dest_file_name,
                save_md5=file_spec.md5_present
            )
        else:
            load_file(
                s3=s3,
                s3_bucket=raw_bucket_name,
                dest_s3_key=dest_s3_key,
                local_file_name=dest_file_name,
                save_md5=file_spec.md5_present
            )


def extract_and_upload_tar_members(dest_s3_prefix: str, member_names: list[str], tar_file_name: str, save_md5: bool):
    with tarfile.open(tar_file_name, 'r') as tar:
        for member in member_names:
            tar.extract(member)
    for member in member_names:
        dest_s3_key = f'{dest_s3_prefix}/{member}'
        load_file(
            s3=s3,
            s3_bucket=raw_bucket_name,
            dest_s3_key=dest_s3_key,
            local_file_name=member,
            save_md5=save_md5
        )


def stream_upload_or_resume_to_s3(dest_s3_key: str, url: str, headers: Any = None, partSizeMb: int = 200, md5: str = None) -> None:
    try:
        s3_client = s3.get_conn()
        parts = []
        part_number = 1
        file_size = 0
        uploaded_bytes = 0
        headers = headers or {}

        # Check if an UploadId already exists to resume download
        upload_id = get_first_s3_multipart_upload_id(s3, raw_bucket_name, dest_s3_key)
        if upload_id:
            # Get the list of already uploaded parts
            dict = s3_client.list_parts(Bucket=raw_bucket_name, Key=dest_s3_key, UploadId=upload_id)
            retrieved_parts = dict.get('Parts', [])
            parts = [{'PartNumber': part['PartNumber'], 'ETag': part['ETag']} for part in retrieved_parts]
            part_number = len(parts) + 1
            uploaded_bytes = sum(part['Size'] for part in retrieved_parts)
            headers['Range'] = f'bytes={uploaded_bytes}-'
        else:
            mpu_response = s3_client.create_multipart_upload(Bucket=raw_bucket_name, Key=dest_s3_key)
            upload_id = mpu_response['UploadId']

        with requests.get(url, stream=True, headers=headers) as r:
            # If resuming, check response status
            if len(parts) > 0 and r.status_code != 206:
                logging.info("File cannot be resumed, starting from the beginning")
                uploaded_bytes = 0
                parts = []
                part_number = 1

            file_size = int(r.headers['Content-Length']) + uploaded_bytes
            r.raise_for_status()

            if uploaded_bytes == 0:
                logging.info(f"Start upload of '{url}' ({bytes_to_human_readable(file_size)}), to {dest_s3_key}")
            else:
                logging.info(f"Resuming upload of '{url}' ({bytes_to_human_readable(file_size)}), to {dest_s3_key} ({bytes_to_human_readable(uploaded_bytes)} already downloaded)")

            for chunk in r.iter_content(chunk_size=partSizeMb * 1024 * 1024):
                if chunk:  # filter out keep-alive new chunks
                    part_response = s3_client.upload_part(
                        Bucket=raw_bucket_name,
                        Key=dest_s3_key,
                        PartNumber=part_number,
                        UploadId=upload_id,
                        Body=chunk
                    )
                    parts.append({'PartNumber': part_number, 'ETag': part_response['ETag']})
                    part_number += 1
                    uploaded_bytes += len(chunk)
                    percentage = (uploaded_bytes / file_size) * 100
                    logging.info(f"Uploaded {bytes_to_human_readable(uploaded_bytes)} of {bytes_to_human_readable(file_size)} ({percentage:.2f}%)")

        # Complete the multipart upload
        s3_client.complete_multipart_upload(
            Bucket=raw_bucket_name,
            Key=dest_s3_key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )
        # Save md5 checksum
        if (md5):
            s3.load_string(md5, f'{dest_s3_key}.md5', raw_bucket_name, replace=True)
            logging.info("Md5 file saved, but not checked (cannot be done on stream upload)")

        logging.info(f"Multipart upload of {dest_s3_key} from {url} completed successfully")

    except Exception as e:
        logging.error(f"Error during multipart upload: {e}")
        raise e
