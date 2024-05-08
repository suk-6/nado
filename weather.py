import requests
import datetime

from config import getENV


class Weather:
    def __init__(self):
        self._url = (
            "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
        )
        self._apiKey = getENV("OPENDATA_API_KEY")
        self._nx = 60
        self._ny = 127
        self._data = None
        self.refreshDate = None

    def getWeather(self):
        if (
            self._data is None
            or self.refreshDate is None
            or self.refreshDate != datetime.datetime.now().strftime("%Y%m%d")
        ):
            self._data = self._fetchWeather()

        temperature = int(
            [item for item in self._data if item["category"] == "TMP"][0]["fcstValue"]
        )
        sky = int(
            [item for item in self._data if item["category"] == "SKY"][0]["fcstValue"]
        )
        rainfall = int(
            [item for item in self._data if item["category"] == "PTY"][0]["fcstValue"]
        )

        # 1: 맑음, 2: 구름, 3: 비, 4: 눈
        sky = 2 if sky == 3 or sky == 4 else 1
        rainfall = 0 if rainfall == 0 else 4 if rainfall == 3 else 3

        if rainfall == 0:
            return {
                "temperature": f"{temperature}°C",
                "sky": sky,
            }
        else:
            return {
                "temperature": temperature,
                "sky": rainfall,
            }

    def _fetchWeather(self):
        now = datetime.datetime.now()
        yesterday = now - datetime.timedelta(days=1)
        baseDate = yesterday.strftime("%Y%m%d")
        baseTime = "2300"

        fcstDate = now.strftime("%Y%m%d")
        fcstTime = now.strftime("%H00")
        self.refreshDate = fcstDate

        params = {
            "serviceKey": self._apiKey,
            "dataType": "JSON",
            "base_date": baseDate,
            "base_time": baseTime,
            "nx": self._nx,
            "ny": self._ny,
            "numOfRows": 300,
            "pageNo": 1,
        }

        res = requests.get(self._url, params=params)
        result = res.json()["response"]["body"]["items"]["item"]
        result = [
            item
            for item in result
            if item["fcstDate"] == fcstDate and item["fcstTime"] == fcstTime
        ]

        return result


if __name__ == "__main__":
    weather = Weather()
    print(weather.getWeather())
