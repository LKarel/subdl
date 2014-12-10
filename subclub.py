import re
from bs4 import BeautifulSoup
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

                for dl_link in soup_new.find_all("a"):
                    result = SubtitleResult("http://subclub.eu" + dl_link.get("href")[2:], 1.0)
                    result.target_name = dl_link.text.strip()
                    ret.append(result)

                    if len(ret) == count:
                        return ret

        return ret
