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
