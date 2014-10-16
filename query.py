import os
import re
import util
from pointer import Pointer

class Query:
    GARBAGE = ["720p", "1080p", "hdtv", "x264"]

    def __init__(self, name):
        self.name = name
        self.pointer = None
        self.keywords = []

    def __str__(self):
        ret = self.name

        if self.pointer:
            ret += " " + str(self.pointer)

        return ret

    def parse(raw, is_file=False):
        raw = raw.lower()

        if is_file:
            # Remove the extension
            raw = os.path.splitext(raw)[0]

        pointer_str = Pointer.read_str(raw)
        name = raw

        if is_file and util.contains_any(["dimension", "killers", "remarkable", "2hd"], raw):
            if pointer_str:
                name = name.split(pointer_str)[0]
        elif pointer_str:
            name = name.replace(pointer_str, "")

        for item in Query.GARBAGE:
            name = name.replace(item, "")

        name = re.sub(r"[.-]", " ", name)
        name = re.sub(r"\s+", " ", name)
        name = name.strip()

        query = Query(name)

        if pointer_str:
            query.pointer = Pointer.parse(pointer_str)

        return query
