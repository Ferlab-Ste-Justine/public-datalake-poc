import hashlib
import re

from airflow.exceptions import AirflowFailException

from lib.utils.http import http_get, http_get_file

def compute_file_md5(path: str, chunk_size: int = 8192) -> str:
    md5 = hashlib.md5()
    with open(path, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_size), b''):
            md5.update(chunk)
        return md5.hexdigest()


def download_and_check_md5(url: str, dest_file_name: str, expected_md5: str) -> str:
    http_get_file(url, dest_file_name)
    md5 = compute_file_md5(dest_file_name)
    if expected_md5 and md5 != expected_md5:
        raise AirflowFailException(f'MD5 checksum verification failed for: {dest_file_name}, expected {expected_md5} but got {md5}')
    return md5


def download_and_parse_md5_file(url: str) -> dict:
    md5_text = http_get(url).text
    md5_hash = re.search('^([0-9a-f]+)', md5_text).group(1)
    return {'hash': md5_hash, 'text': md5_text}