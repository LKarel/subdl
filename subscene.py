import re
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import http.client, urllib.parse
from query import Query
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

    def _extract_rating(self, input):
        match = re.match(r".*(?P<rating>\d+)", input)

        if match:
            return int(match.group("rating"))

        return 0

    def find(self, query, lang=None):
        lang = self._convert_lang(lang)

        if not query.filename:
            search = str(query)
        else:
            search = query.filename

        params = urllib.parse.urlencode({"q": search})

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

            link_name = sub.find_all("span")[1].contents[0].strip()
            link_pointer = Query.parse(link_name).pointer

            if str(link_pointer) != str(query.pointer):
                continue

            if sub.get("href") not in sub_links:
                sub_links.append({
                    "filename": link_name + ".srt",
                    "url": sub.get("href"),
                    "score": SequenceMatcher(None, query.filename, link_name).ratio()
                })

        sub_links = sorted(sub_links, key=lambda v: v["score"], reverse=True)
        ret = []
        i = 0

        for item in sub_links:
            soup = util.connect("subscene.com", item["url"])
            dl_button = soup.find(id="downloadButton")
            dl_link = dl_button.get("href")

            rating = 0
            rating_title = soup.find("span", class_="rating-bar")

            if rating_title:
                rating = self._extract_rating(rating_title["title"])

            score = (rating / 10) * 0.15 + 0.6 * item["score"]
            result = SubtitleResult("http://subscene.com" + dl_link, score)
            result.target_name = item["filename"]
            result.zipped = True

            ret.append(result)
            i += 1
            if i == 10:
                break

        return ret
