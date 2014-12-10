import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import urllib.parse
from subtitle_result import SubtitleResult
from subtitle_source import SubtitleSource
import util

class SubClub(SubtitleSource):
    def _get_subid(self, url):
        match = re.match(r".*[?&]id=(?P<id>\d+)", url)

        if match:
            return match.group("id")

    def find(self, query, count=1, lang=None):
        if lang != "et":
            # Subclub has only Estonian subtitles
            return []

        params = {
            "otsing": query.name,
            "tp": "nimi"
        }

        if query.imdb:
            params["otsing"] = str(query.imdb)
            params["tp"] = "kood"
        elif query.pointer:
            params["otsing"] += " %sx%s" % (query.pointer.season, query.pointer.episode)

        params = urllib.parse.urlencode(params)
        soup = util.connect("subclub.eu", "/jutud.php?" + params)

        ret = []

        for link in soup.find_all("a"):
            url = link.get("href")
            if "down.php" in url:
                subid = self._get_subid(url)

                if not subid:
                    continue

                soup_new = util.connect("subclub.eu", "/subtitles_archivecontent.php?id=" + subid)

                for anchor in soup_new.find_all("a"):
                    dl = "http://subclub.eu%s" % anchor.get("href")[2:]
                    filename = anchor.text.strip()
                    score = 0.4 + 0.6 * SequenceMatcher(None, query.filename, filename).ratio()

                    result = SubtitleResult(dl, score)
                    result.target_name = filename
                    ret.append(result)

        return ret
