import os
import re
import urllib.parse
import util
from pointer import Pointer

class Query:
    def __init__(self, name):
        self._imdb = None

        self.name = name
        self.filename = None
        self.pointer = None

    def imdb(self):
        if not self._imdb:
            query = urllib.parse.quote(str(self))
            soup = util.connect("www.imdb.com", "/find?q=%s" % query)

            for a in soup.select("tr.findResult td.result_text a"):
                href = a.get("href")

                if not href.startswith("/title/"):
                    continue

                match = re.match(r"^/title/(?P<id>\w+)/", href)

                if not match:
                    continue

                self._imdb = match.group("id")
                break

        return self._imdb

    def __str__(self):
        ret = self.name

        if self.pointer:
            ret += " " + str(self.pointer)

        return ret

    def parse(filename):
        filename = filename.lower()
        filename = os.path.splitext(filename)[0]

        name = filename
        pointer_str = Pointer.read_str(filename)

        if pointer_str:
            name = filename.split(pointer_str)[0]

        name = re.sub(r"[.-]", " ", name)
        name = re.sub(r"\s+", " ", name)
        name = name.strip()

        # It is a movie
        if not pointer_str:
            name = re.sub(r"^(.+\d{4}).*$", r"\1", name)

        query = Query(name)
        query.filename = filename

        if pointer_str:
            query.pointer = Pointer.parse(pointer_str)

        return query
