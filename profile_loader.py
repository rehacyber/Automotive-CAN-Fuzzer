import json


class ProfileLoader:

    def __init__(self, profile_path):

        self.profile_path = profile_path



    def load(self):

        with open(
            self.profile_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)