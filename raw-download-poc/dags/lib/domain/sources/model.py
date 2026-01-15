from dataclasses import dataclass
from typing import Optional, List

from datetime import timedelta


@dataclass(frozen=True)
class FileSpec:
    name: str
    headers: Optional[dict] = None
    extract_members: Optional[List[str]] = None,
    streaming: bool = False,
    md5_present: bool = False

    def __init__(
        self,
        name: str = None,
        url: Optional[str] = None,
        url_fn: Optional[callable] = None,
        headers: Optional[dict] = None,
        extract_members: Optional[List[str]] = None,
        streaming: bool = False,
        md5_present: bool = False
    ):
        assert url or url_fn, "Either url or url_fn must be provided"
        assert not (url and url_fn), "Specify only one of url or url_fn"
        assert not (streaming and extract_members), "streaming does not support tar extract"

        object.__setattr__(self, "_url", url)
        object.__setattr__(self, "_url_fn", url_fn)
        object.__setattr__(self, "headers", headers)
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "extract_members", extract_members)
        object.__setattr__(self, "streaming", streaming)
        object.__setattr__(self, "md5_present", md5_present)

    def get_md5_url(self) -> Optional[str]:
        if not self.md5_present:
            return None
        file_url = self.get_url()
        return file_url + ".md5" if file_url else None

    def get_url(self) -> str:
        return self._url if self._url else self._url_fn()

    @property
    def tar_extract(self) -> bool:
        return bool(self.extract_members)


@dataclass(frozen=True)
class DownloadConfig:
    poll_interval: Optional[timedelta]
    files: List[FileSpec]


@dataclass(frozen=True)
class SourceMeta:
    short_name: str
    display_name: str
    website: str
    download_config: DownloadConfig
