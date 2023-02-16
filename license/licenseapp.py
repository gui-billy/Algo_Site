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


@app.get("/mt5")
async def login(data: LoginData):
    for cred in CREDENTIALS:
        if data.username == cred["username"] and data.password == \
                cred["password"]:
            return {
                print('Login ok')
            }
