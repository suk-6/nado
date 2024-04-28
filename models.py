from pydantic import BaseModel
from typing import Union


class UserModel(BaseModel):
    id: int
    kakaoUID: Union[str, None]
    image: Union[str, None]
    nickname: Union[str, None]
    region: Union[str, None]


class ClubModel(BaseModel):
    id: int
    name: str
    image: str
    owner: int
    users: str
