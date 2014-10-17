import os
import re
import util
from pointer import Pointer

class Query:
    def __init__(self, name):
        self.name = name
        self.filename = None
        self.pointer = None

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

        query = Query(name)
        query.filename = filename

        if pointer_str:
            query.pointer = Pointer.parse(pointer_str)

        print(query.name, query.pointer)

        return query
