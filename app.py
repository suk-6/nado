import os
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from board import Board
from lecture import Lecture
from interview import Interview
from gaze import GazeAnalysis
from resume import Resume
from stt import STT
from openaic import OpenAIClass
from weather import Weather
from dto import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    os.system("rm -rf /tmp/*.mp3")
    os.system("rm -rf /tmp/*.mp4")
    os.system("rm -rf /tmp/*.html")
    os.system("rm -rf /tmp/*.pdf")


app = FastAPI(lifespan=lifespan)
openai = OpenAIClass()
stt = STT(openai())
board = Board()
resume = Resume(openai())
lecture = Lecture()
interview = Interview(openai())
weather = Weather()


@app.get("/weather")
async def getWeather():
    return weather.getWeather()


# 강의 엔드포인트
@app.get("/lecture/get/{courceType}")
async def getLecture(courceType: str):
    return lecture.getLecture(courceType)


@app.get("/lecture/get/{courceType}/{count}")
async def getLecture(courceType: str, count: int):
    return lecture.getLecture(courceType, count)


# 게시판 엔드포인트
@app.get("/board/get")
async def getBoard():
    return board.getBoard()


@app.get("/board/delete/{id}")
async def deleteBoard(id: int, password: str):
    return board.deleteBoard(id, password)


# 게시물 엔드포인트
@app.get("/post/get")
async def getPost(postID: int = None, boardID: int = None):
    return board.getPost(postID, boardID)


@app.post("/post/create")
async def createPost(post: PostCreateDTO):
    return board.createPost(post.title, post.content, post.board, post.password)


@app.get("/comment/get")
async def getComment(postID: int):
    return board.getComment(postID)


@app.post("/comment/add")
async def addComment(comment: CommentAddDTO):
    return board.addComment(comment.postID, comment.commentID, comment.content)


# 자기소개서 엔드포인트
@app.post("/resume/pdf")
async def generateResumePDF(data: ResumePDFDTO):
    pdf = resume.pdf(data.name, data.content)
    return FileResponse(f"/tmp/{pdf.rand}.pdf")


@app.post("/resume/gpt")
async def generateResumeGPT(data: ResumeGPTDTO):
    return resume.generateResume(data.keywords)


@app.post("/resume/spelling")
async def checkSpelling(data: ResumeSpellingDTO):
    return resume.checkSpelling(data.content)


# 질문 엔드포인트
@app.get("/interview/q/get")
async def getInterviewQuestion():
    return interview.getInterviewQuestion()


# 시선 분석 엔드포인트
# 비디오 파일 업로드
@app.post("/interview/analysis")
async def analysisInterview(file: UploadFile):
    gaze = GazeAnalysis()

    with open(gaze.videoPath, "wb") as f:
        f.write(file.file.read())

    gazeResult = gaze.analysis()

    stt.mp4tomp3(gaze.id)
    text = stt(f"/tmp/{gaze.id}.mp3")
    del gaze

    percent = int((len(gazeResult) / 100) * 30)
    if gazeResult.count("right") + gazeResult.count("left") > percent:
        gazeResult = "Looking elsewhere"
    else:
        gazeResult = "Looking at the camera"

    result = {
        "gaze tracking result": gazeResult,
        "interviewer": text,
    }

    return interview.interviewAnalysis(result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", reload=True)
