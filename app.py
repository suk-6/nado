from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from club import Club
from auth import Auth
from config import getENV
from lecture import Lecture
from dto import *
from models import *

app = FastAPI()
auth = Auth()
club = Club()
lecture = Lecture()

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")


async def getLoginUser(token: Annotated[str, Depends(oauth2Scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, getENV("JWT_SECRET"), algorithms="HS256")
        userID: int = payload.get("userID")
        if userID is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = auth.getUser(userID=userID)
    if user is None:
        raise credentials_exception
    return user


@app.get("/login")
async def login(code: str):
    token = auth.login(code)

    return {"token": token}


@app.get("/user/me")
async def me(user: Annotated[UserModel, Depends(getLoginUser)]):
    return user


@app.get("/user/nickname")
async def updateNickname(
    nickname: str, user: Annotated[UserModel, Depends(getLoginUser)]
):
    return auth.updateNickname(user.id, nickname)


@app.get("/user/region")
async def updateRegion(region: str, user: Annotated[UserModel, Depends(getLoginUser)]):
    return auth.updateRegion(user.id, region)


@app.get("/lecture/get/{courceType}")
async def getLecture(courceType: str):
    return lecture.getLecture(courceType)


@app.get("/club/get")
async def getClub():
    return club.getClub()


@app.post("/club/create")
async def createClub(
    clubCreateDTO: ClubCreateDTO, user: Annotated[UserModel, Depends(getLoginUser)]
):
    return club.createClub(clubCreateDTO.name, clubCreateDTO.image, user.id)


@app.get("/club/join/{clubID}")
async def joinClub(clubID: int, user: Annotated[UserModel, Depends(getLoginUser)]):
    return club.joinClub(clubID, user.id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", reload=True)
