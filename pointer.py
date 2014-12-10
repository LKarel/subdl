import re

class Pointer:
    def __init__(self, season, episode):
        self.season = season
        self.episode = episode

    def __str__(self):
        return "S%02iE%02i" % (self.season, self.episode)

    def __eq__(self, other):
        return self.season == other.season and self.episode == other.episode

    def parse(raw):
        regex = None

        if raw[0] == "s":
            regex = r"^s(?P<season>\d{2})e(?P<episode>\d{2})"
        elif raw.lower().find("x") != -1:
            regex = r"^(?P<season>\d+)x(?P<episode>\d+)"

        if not regex:
            return

        result = re.match(regex, raw.lower())

        if result:
            return Pointer(int(result.group("season")), int(result.group("episode")))

    def read_str(data):
        result = re.match(r".*(?P<pointer>s\d+e\d+|\d+x\d+).*", data.lower())
        if result:
            return result.group("pointer")
