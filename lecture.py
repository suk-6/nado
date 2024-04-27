import datetime
import requests
from config import getENV


class Lecture:
    def __init__(self):
        self.apiURL = f"http://openAPI.seoul.go.kr:8088/{getENV('API_KEY')}/json"

        self.data = {}
        self.renewTime = None

    def getLecture(self, courceType="OnlineCoures"):
        if (
            self.renewTime is None
            or self.renewTime + datetime.timedelta(hours=1) < datetime.datetime.now()
            or self.data == {}
        ):
            self.renewTime = datetime.datetime.now()
            self.data[courceType] = self._getLecture(courceType)[courceType]["row"]

        return self.data

    def _getLecture(self, courceType):
        url = f"{self.apiURL}/{courceType}"
        list_total_count = requests.get(f"{url}/1/1").json()[courceType][
            "list_total_count"
        ]
        return requests.get(f"{url}/1/{list_total_count}").json()


if __name__ == "__main__":
    Lecture()
