from bs4 import BeautifulSoup
import http.client, urllib.parse
from subtitle_result import SubtitleResult
from subtitle_source import SubtitleSource
import util

class SubScene(SubtitleSource):
    def __convertLang(self, lang):
        langs = {'et': 'estonian', 'en': 'english'}
        if lang in langs:
            return langs[lang]
        else:
            return 'english'

    def find(self, query, count=1, lang=None):
        lang = self.__convertLang(lang)

        search = query.name

        if query.pointer:
            search += " %s" % str(query.pointer)

        params = urllib.parse.urlencode({"q": search,})

        sub_links = []

        if not query.pointer:
            soup = util.connect("subscene.com", "/subtitles/title?" + params)

            for link in soup.find_all("a"):
                if not link.string:
                    continue

                if query.name not in link.string.lower():
                    continue

                subs_list = link.get("href")
                soup_new = util.connect("subscene.com", subs_list)

                for sub in soup_new.find_all("a"):
                    if lang not in sub.get("href"):
                        continue

                    if sub.get("href") not in sub_links:
                        sub_links.append(sub.get("href"))

                    if len(sub_links) == count:
                        break

                if len(sub_links) == count:
                    break
        else:
            soup = util.connect("subscene.com", "/subtitles/release?" + params)

            for sub in soup.find_all("a"):
                if lang not in sub.get("href"):
                    continue

                for span in sub.find_all("span"):
                    if str(query.pointer).upper() not in span.string.upper():
                        continue

                    if sub.get("href") not in sub_links:
                        sub_links.append(sub.get("href"))

                    if len(sub_links) == count:
                        break

        print(sub_links)

        return 0

        ret = []

        for link in soup.find_all("a"):
            url = link.get("href")
            if query.name in url:
                subid = self._get_subid(url)

                soup_new = util.connect("http://subscene.com/", "/subtitles_archivecontent.php?id=" + subid)

                for dl_link in soup_new.find_all("a"):
                    dl_url = dl_link.get("href")
                    ret.append(SubtitleResult("http://subclub.eu" + dl_url[2:], 1.0))
                
                    if len(ret) == count:
                        return ret
            
        return ret
