import os
import re
import urllib.parse
import util
from pointer import Pointer

class Query:
    def __init__(self, name):
        self.name = name
        self.filename = None
        self.pointer = None
        self.imdb = None

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
        query.imdb = Query._get_imdb_id(name)

        if pointer_str:
            query.pointer = Pointer.parse(pointer_str)

        return query

    def _get_imdb_id(query):
        query = urllib.parse.quote(query)
        soup = util.connect("www.imdb.com", "/find?q=%s" % query)

        for a in soup.select("tr.findResult td.result_text a"):
            href = a.get("href")

            if not href.startswith("/title/"):
                continue

            match = re.match(r"^/title/(?P<id>\w+)/", href)

            if not match:
                continue

            return match.group("id")
