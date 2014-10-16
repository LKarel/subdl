import os.path

class SubtitleResult:
    def __init__(self, url, score):
        self.score = score
        self.download_url = url
        self.target_name = None

    def get_target_name(self):
        if self.target_name:
            return self.target_name

        return os.path.basename(self.download_url.split("?")[0])
