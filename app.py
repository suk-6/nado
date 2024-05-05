from fastapi import FastAPI

from board import Board
from config import getENV
from lecture import Lecture
from interview import Interview
from dto import *

# from models import *

app = FastAPI()
board = Board()
lecture = Lecture()
interview = Interview()


# 강의 엔드포인트
@app.get("/lecture/get/{courceType}")
async def getLecture(courceType: str):
    return lecture.getLecture(courceType)


# 게시판 엔드포인트
@app.get("/board/get")
async def getBoard():
    return board.getBoard()


# 게시물 엔드포인트
@app.get("/post/get")
async def getPost():
    return board.getPost()


@app.post("/post/create")
async def createPost(post: PostCreateDTO):
    return board.createPost(post.title, post.content, post.board, post.password)


# 질문 엔드포인트
@app.get("/interview/q/get")
async def getInterviewQuestion():
    return interview.getInterviewQuestion()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", reload=True)
