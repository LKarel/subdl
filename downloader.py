import http
import os
import zipfile
import tempfile
import util
from subtitle_file import SubtitleFile

class Downloader:
    def __init__(self, sources):
        self.sources = sources

    def get(self, query, count=1, lang=None):
        files = []
        results = []

        for source in self.sources:
            results += source.find(query, lang=lang)

        results = sorted(results, key=lambda v: v.score, reverse=True)

        for result in results:
            extension = os.path.splitext(result.download_url)[1]
            target_name = result.get_target_name()
            body = util.download_bytes(result.download_url)

            if not body:
                continue

            if result.zipped:
                tmp = tempfile.TemporaryFile()
                tmp.write(body)

                try:
                    z = zipfile.ZipFile(tmp)
                except zipfile.BadZipFile:
                    continue

                names = z.namelist()
                if len(names) == 0:
                    continue

                body = z.read(names[0])
                target_name = names[0]

            files.append(SubtitleFile(target_name, body))

            if len(files) == count:
                break

        return files
