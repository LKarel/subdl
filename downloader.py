import http
import os
import zlib
import util
from subtitle_file import SubtitleFile

class Downloader:
    def __init__(self, sources):
        self.sources = sources

    def get(self, query, count=1, lang=None):
        files = []
        results = []

        for source in self.sources:
            results += source.find(query, count, lang)

        results = sorted(results, key=lambda v: v.score, reverse=True)

        for result in results:
            extension = os.path.splitext(result.download_url)[1]
            body = util.download_bytes(result.download_url)

            if not body:
                continue

            files.append(SubtitleFile(result.get_target_name(), body))

            if len(files) == count:
                break

        if len(files) >= count:
            return files[:count]

        return files
