from lib.domain.sources.definitions import SOURCES_META, Source


class SourceRegistry:
    @staticmethod
    def get_download_config(source: Source):
        source_meta = SOURCES_META.get(source)
        if source_meta is None:
            raise ValueError(f"Source {source} not found in registry.")
        return source_meta.download_config

    @staticmethod
    def get_source_id(source: Source) -> str:
        return source.value
