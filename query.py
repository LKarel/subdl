import re
from pointer import Pointer

class Query:
    KEYWORDS = ["yifi", "publichd", "norar"]

    def __init__(self, name, pointer=None):
        self.name = name
        self.pointer = pointer
        self.keywords = []

    def __str__(self):
        ret = self.name

        if self.pointer:
            ret += " " + str(self.pointer)

        return ret

    def parse(raw):
        result = re.match(r'^(?P<name>.+)(?P<pointer>S\d{2}E\d{2}|\d+x\d+)?', raw)

        if not result.group("name"):
            return

        name = result.group("name").replace(".", " ").strip()
        pointer = None
        kws = []

        for kw in KEYWORDS:
            if name.lower().find(kw) != -1:
                kws.append(kw)

        if result.group("pointer"):
            pointer = Pointer.parse(result.group("pointer"))

        return Query(name, pointer=pointer)
