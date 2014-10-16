from bs4 import BeautifulSoup
import urllib.parse
from subtitle_result import SubtitleResult
from subtitle_source import SubtitleSource
import util

class SubClub(SubtitleSource):
    def _get_subid(self, url):
        subid = ''
        for ch in url:
            if ch.isdigit():
                subid += ch

        return subid

    def find(self, query, count=1, lang=None):
        if lang != "et":
            # Subclub has only Estonian subtitles
            return []

        search = query.name

        if query.pointer:
            search += " %sx%s" % (query.pointer.season, query.pointer.episode)

        params = urllib.parse.urlencode({"otsing": search,})

        soup = util.connect("subclub.eu", "/jutud.php?" + params)

        ret = []

        for link in soup.find_all("a"):
            url = link.get("href")
            if "down.php" in url:
                subid = self._get_subid(url)

                soup_new = util.connect("subclub.eu", "/subtitles_archivecontent.php?id=" + subid)

                for dl_link in soup_new.find_all("a"):
                    result = SubtitleResult("http://subclub.eu" + dl_link.get("href")[2:], 1.0)
                    result.target_name = dl_link.text.strip()
                    ret.append(result)

                    if len(ret) == count:
                        return ret

        return ret
