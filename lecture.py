from random import sample
import datetime
import requests
from config import getENV


class Lecture:
    def __init__(self):
        self.apiURL = f"http://openAPI.seoul.go.kr:8088/{getENV('API_KEY')}/json"
        self.onlineCourseURL = "https://sll.seoul.go.kr/lms/requestCourse/doDetailInfo.do?course_id={}&course_gubun=1"
        self.onlineCourseCategory = {
            "전문자격증": [
                "공인중개사",
                "주택관리사",
                "직업상담사",
                "전기기능사/기사",
                "조리/미용",
                "사회복지사",
                "기타",
            ],
            "디지털": [
                "전문기술과정",
                "방송/영상",
                "AR/VR",
                "인공지능",
                "웹툰/이모티콘",
                "콘텐츠산업",
                "전문과정",
                "취미파이프라인(디지털)",
            ],
            "직무역량개발": ["직무역량과정", "경영일반", "금융/회계"],
            "창업": ["창업과정", "마케팅", "취미파이프라인(창업)"],
            "리더십": ["리더십/인사조직", "셀프브랜딩"],
        }

        self.data = {}
        self.renewTime = None

    def getLecture(self, courceType="OnlineCoures", count=None):
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

                    for key, value in self.onlineCourseCategory.items():
                        if self.data[courceType][i]["CATEGORY_NM2"] in value:
                            self.data[courceType][i]["category"] = key

                    if self.data[courceType][i].get("category") is None:
                        self.data[courceType][i]["category"] = "기타"

        if count is None:
            return self.data[courceType]
        else:
            return sample(self.data[courceType], count)

    def _getLecture(self, courceType):
        url = f"{self.apiURL}/{courceType}"
        list_total_count = requests.get(f"{url}/1/1").json()[courceType][
            "list_total_count"
        ]
        return requests.get(f"{url}/1/{list_total_count}").json()


if __name__ == "__main__":
    print(Lecture().getLecture()["OnlineCoures"][0])
