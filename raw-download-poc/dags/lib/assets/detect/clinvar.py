import re
from typing import Any, Optional

from lib.domain.events.triggers import HttpEventTrigger
from lib.domain.catalog import get_current_version
from lib.domain.sources.definitions import Source
from lib.domain.sources.registry import SourceRegistry
from lib.domain.events.base import version_change_payload


class ClinvarTrigger(HttpEventTrigger):

    def __init__(self):
        download_config = SourceRegistry.get_download_config(Source.CLINVAR)
        super().__init__(
            url=download_config.files[0].get_md5_url(),
            poll_interval=download_config.poll_interval.total_seconds()
        )

    def serialize(self) -> tuple[str, dict[str, Any]]:
        return (
            self.__class__.__module__ + "." + self.__class__.__qualname__,
            {},
        )

    async def check_response(self, text) -> Optional[dict]:
        latest_version = re.search(r'clinvar_([0-9]+)\.vcf', text).group(1)
        current_version = await get_current_version(Source.CLINVAR)
        if latest_version != current_version:
            return version_change_payload(
                source=Source.CLINVAR,
                current_version=current_version,
                latest_version=latest_version
            )
        return None
