from bs4 import BeautifulSoup
import http.client, urllib.parse
from subtitle_result import SubtitleResult
from subtitle_source import SubtitleSource

class SubClub(SubtitleSource):
    def find(self, query, count=1, lang=None):
        if lang != "et":
            # Subclub has only Estonian subtitles
            return []

        search = query.name

        if query.pointer:
            search += " %sx%s" % (query.pointer.season, query.pointer.episode)

        params = urllib.parse.urlencode({"otsing": search,})

        connect = http.client.HTTPConnection("subclub.eu")
        connect.request("GET", "/jutud.php?" + params)
        response = connect.getresponse()

        soup = BeautifulSoup(response.read())
        ret = []

        for link in soup.find_all("a"):
            url = link.get("href")
            if "down.php" in url:
                ret.append(SubtitleResult("http://subclub.eu" + url[2:], 1.0))

                if len(ret) == count:
                    break

        return ret
