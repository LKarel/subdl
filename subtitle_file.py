import os

class SubtitleFile:
    def __init__(self, name, body):
        self.name = name
        self.body = body

    def write(self, parent):
        path = os.path.join(parent, self.name)
        fh = open(path, "wb")
        fh.write(self.body)
        fh.close()

        return path
