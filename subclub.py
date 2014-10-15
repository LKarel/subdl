from bs4 import BeautifulSoup
import http.client, urllib.parse
from subtitle_source import SubtitleSource

class subclub(SubtitleSource):
    def find(self, query, count=1, lang=None):
        search = query.name

        if query.pointer:
            search += " %sx%s" % (query.pointer.season, query.pointer.episode)

        params = urllib.parse.urlencode({"otsing": search,})

        connect = http.client.HTTPConnection("subclub.eu")
        connect.request("GET", "/jutud.php?" + params)
        response = connect.getresponse()

        soup = BeautifulSoup(response.read())

        for link in soup.find_all("a"):
            url = link.get("href")
            if "down.php" in url:
                return 'subclub.eu%s' % url[2:]

        return None
