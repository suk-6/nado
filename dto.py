from pydantic import BaseModel


class ClubCreateDTO(BaseModel):
    name: str
    image: str  # base64


class PostCreateDTO(BaseModel):
    title: str
    content: str
    board: int
