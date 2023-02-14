from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

exp = datetime(2023, 5, 1)

CREDENTIALS = [
    {"username": "user1", "password": "password1"}
]


class LoginData(BaseModel):
    username: str
    password: str


app = FastAPI()


for cred in CREDENTIALS:
    print(cred)
