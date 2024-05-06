from pydantic import BaseModel


class PostCreateDTO(BaseModel):
    title: str
    content: str
    board: int
    password: str


class ResumePDFDTO(BaseModel):
    name: str
    content: str


class ResumeGPTDTO(BaseModel):
    keywords: str


class ResumeSpellingDTO(BaseModel):
    content: str


class CommentAddDTO(BaseModel):
    postID: int
    commentID: int
    content: str
