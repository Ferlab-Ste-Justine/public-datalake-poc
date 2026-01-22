from lib.domain.sources.definitions import Source


class SourceRegistry:
    @staticmethod
    def get_source_id(source: Source) -> str:
        return source.value
