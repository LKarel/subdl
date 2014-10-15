import re

class Pointer:
    def __init__(self, season, episode):
        self.season = season
        self.episode = episode

    def __str__(self):
        return "S%02iE%02i" % (self.season, self.episode)

    def parse(raw):
        regex = None

        if raw[0] == "S":
            regex = r"^S(?P<season>\d{2})E(?P<episode>\d{2})"
        elif raw.lower().find("x") != -1:
            regex = r"^(?P<season>\d+)[xX](?P<episode>\d+)"

        if not regex:
            return

        result = re.match(regex, raw)

        if result:
            return Pointer(int(result.group("season")), int(result.group("episode")))

    def read_str(data):
        result = re.match(r".*(?P<pointer>s\d+e\d+|\d+x\d+).*", data.lower())
        if result:
            return result.group("pointer")
