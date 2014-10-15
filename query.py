import os
import re
from pointer import Pointer

class Query:
    KEYWORDS = ["yifi", "publichd", "norar"]

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
            raw = os.path.splitext(raw)[0]

        pointer_str = Pointer.read_str(raw)

        name = raw
        pointer = None
        kws = []

        if pointer_str:
            pointer = Pointer.parse(pointer_str)
            name = name.replace(pointer_str, "")

        for kw in Query.KEYWORDS:
            if raw.lower().find(kw) != -1:
                kws.append(kw)

        # TODO: Specifically handle names in known format
        name = re.sub(r"[.-]", " ", name)
        name = re.sub(r"\s+", " ", name)
        name = name.strip()

        query = Query(name)
        query.pointer = pointer
        query.keywords = kws

        return query
