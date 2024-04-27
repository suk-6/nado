from fastapi import FastAPI

from lecture import Lecture
from auth import Auth

app = FastAPI()
auth = Auth()
lecture = Lecture()


@app.get("/login")
async def login(code: str):
    kakaoUser = auth.getKakaoUserInfo(code)
    token = auth.login(kakaoUser["id"])

    return {"token": token}


@app.get("/get/lecture/{courceType}")
async def getLecture(courceType: str):
    return lecture.getLecture(courceType)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
