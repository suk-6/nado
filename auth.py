import requests
from jose import JWTError, jwt

from config import getENV
from db import DB


class Auth:
    def __init__(self):
        self.db = DB()

    def login(self, code):
        if code == getENV("TEST_CODE"):
            user = self.db.createUser("test")
            return self.createToken(user.id)

        kakaoUser = self.getKakaoUserInfo(code)
        user = self.db.createUser(kakaoUser["id"])
        return self.createToken(user.id)

    def createToken(self, userID):
        data = {"userID": userID}
        token = jwt.encode(data, getENV("JWT_SECRET"), algorithm="HS256")

        return token

    def getKakaoUserInfo(accessToken: str):
        url = getENV("KAKAO_USERINFO_URL")
        headers = {"Authorization": f"Bearer {accessToken}"}

        return requests.get(url, headers=headers).json()

    def getUser(self, userID):
        return self.db.getUser(userID)
