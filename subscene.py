from bs4 import BeautifulSoup
import http.client, urllib.parse
from subtitle_result import SubtitleResult
from subtitle_source import SubtitleSource
import util

class SubScene(SubtitleSource):
    def _convert_lang(self, lang):
        langs = {'et': 'estonian', 'en': 'english'}
        if lang in langs:
            return langs[lang]
        else:
            return 'english'

    def _find_movie_by_name(self, query, soup):
        sub_links = []

        for link in soup.find_all("a"):
            if not link.string:
                continue

            if query.name not in link.string.lower():
                continue

            return link.get("href")

    def find(self, query, count=1, lang=None):
        lang = self._convert_lang(lang)

        if not query.filename:
            search = query.name

            if query.pointer:
                search += " %s" % str(query.pointer)
        else:
            search = query.filename

        params = urllib.parse.urlencode({"q": search,})

        if not query.pointer and not query.filename:
            soup = util.connect("subscene.com", "/subtitles/title?" + params)
            sub_links_page = self._find_movie_by_name(query, soup)
        else:
            sub_links_page = "/subtitles/release?" + params

        soup = util.connect("subscene.com", sub_links_page)

        sub_links = []

        for sub in soup.find_all("a"):
            if lang not in sub.get("href"):
                continue

            for span in sub.find_all("span"):
                if sub.get("href") not in sub_links:
                    sub_links.append(sub.get("href"))

                if len(sub_links) == count:
                    break

            if len(sub_links) == count:
                break

        ret = []

        for link in sub_links:
            soup = util.connect("subscene.com", link)
            dl_button = soup.find(id="downloadButton")
            dl_link = dl_button.get("href")

            rating = ''
            rating_title = soup.find("span", class_="rating-bar")

            for ch in rating_title['title']:
                if ch.isdigit():
                    rating += ch

            rating = (int(rating) / 10) * 0.75
            ret.append(SubtitleResult(dl_link, rating))

        return ret
