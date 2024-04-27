import requests
from jose import JWTError, jwt

from config import getENV
from db import DB


class Auth:
    def __init__(self):
        self.db = DB()

    def login(self, userID):
        userID = self.db.getUser(userID)
        return self.createToken(userID)

    def createToken(self, userID):
        data = {"userID": userID}
        token = jwt.encode(data, getENV("JWT_SECRET"), algorithm="HS256")

        return token

    def getKakaoUserInfo(accessToken: str):
        url = getENV("KAKAO_USERINFO_URL")
        headers = {"Authorization": f"Bearer {accessToken}"}

        return requests.get(url, headers=headers).json()
