from random import sample
import datetime
import requests
from config import getENV


class Lecture:
    def __init__(self):
        self.apiURL = f"http://openAPI.seoul.go.kr:8088/{getENV('API_KEY')}/json"
        self.onlineCourseURL = "https://sll.seoul.go.kr/lms/requestCourse/doDetailInfo.do?course_id={}&course_gubun=1"
        self.onlineCourseCategory = {
            "법정의무": ["인권", "공인중개사 연수교육", "금융", "기타", "금융/회계"],
            "인문/교양": [
                "인문학",
                "사회/교양",
                "취미생활",
                "문화예술",
                "경영일반",
                "취미생활",
            ],
            "외국어": ["영어", "일본어", "중국어", "기타외국어"],
            "가족/건강": ["건강관리", "부모교육", "아동/청소년"],
            "정보/컴퓨터": [
                "소셜미디어",
                "멀티미디어",
                "프로그래밍",
                "OA활용",
                "신기술교육",
                "방송/영상",
                "웹툰/이모티콘",
                "AR/VR",
                "인공지능",
                "콘텐츠산업 전문과정",
            ],
            "자격증": [
                "국가공인민간자격",
                "국가기술자격",
                "국가전문자격",
                "기타자격",
                "직업상담사",
                "공인중개사",
                "주택관리사",
                "사회복지사",
                "공인중개사 연수교육",
                "기타",
            ],
            "취/창업": [
                "창업",
                "취업",
                "시니어취업",
                "창업과정",
                "직무역량과정",
                "리더십/인사조직",
                "셀프브랜딩",
                "시민제작",
                "전문기술과정",
            ],
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

                    if self.data[courceType][i]["CATEGORY_NM2"] == "기타":
                        self.data[courceType][i]["category"] = "기타"
                    else:
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
