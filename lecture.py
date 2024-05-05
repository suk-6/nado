import datetime
import requests
from config import getENV


class Lecture:
    def __init__(self):
        self.apiURL = f"http://openAPI.seoul.go.kr:8088/{getENV('API_KEY')}/json"
        self.onlineCourseURL = "https://sll.seoul.go.kr/lms/requestCourse/doDetailInfo.do?course_id={}&course_gubun=1"

        self.data = {}
        self.renewTime = None

    def getLecture(self, courceType="OnlineCoures"):
        if (
            self.renewTime is None
            or self.renewTime + datetime.timedelta(hours=1) < datetime.datetime.now()
            or self.data == {}
            or self.data.get(courceType) is None
        ):
            self.renewTime = datetime.datetime.now()
            self.data[courceType] = self._getLecture(courceType)[courceType]["row"]

            if courceType == "OnlineCoures":
                for i in range(len(self.data[courceType])):
                    self.data[courceType][i]["link"] = self.onlineCourseURL.format(
                        self.data[courceType][i]["COURSE_ID"]
                    )

        return self.data[courceType]

    def _getLecture(self, courceType):
        url = f"{self.apiURL}/{courceType}"
        list_total_count = requests.get(f"{url}/1/1").json()[courceType][
            "list_total_count"
        ]
        return requests.get(f"{url}/1/{list_total_count}").json()


if __name__ == "__main__":
    print(Lecture().getLecture()["OnlineCoures"][0])
