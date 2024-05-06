import urllib
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse

from board import Board
from config import getENV
from lecture import Lecture
from interview import Interview
from gaze import GazeAnalysis
from resume import Resume
from stt import STT
from openaic import OpenAIClass
from dto import *

# from models import *

app = FastAPI()
openai = OpenAIClass()
stt = STT(openai())
board = Board()
resume = Resume(openai())
lecture = Lecture()
interview = Interview()


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


# 게시물 엔드포인트
@app.get("/post/get")
async def getPost():
    return board.getPost()


@app.post("/post/create")
async def createPost(post: PostCreateDTO):
    return board.createPost(post.title, post.content, post.board, post.password)


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
    content = urllib.parse.quote(data.content)
    return resume.checkSpelling(resume.checkSpelling(content))


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
    del gaze

    stt.mp4tomp3(gaze.id)
    text = stt(f"/tmp/{gaze.id}.mp3")

    percent = int((len(gazeResult) / 100) * 30)
    if gazeResult.count("right") + gazeResult.count("left") > percent:
        gazeResult = "Looking elsewhere"
    else:
        gazeResult = "Looking at the camera"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", reload=True)
