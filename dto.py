from pydantic import BaseModel


class ClubCreateDTO(BaseModel):
    name: str
    image: str  # base64
