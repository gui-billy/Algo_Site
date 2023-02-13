import secrets
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

secret = secrets.token_hex(32)
CREDENTIALS = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"}
]


class LoginData(BaseModel):
    username: str
    password: str


app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/login")
async def login(data: LoginData):

    for cred in CREDENTIALS:
        if data.username == cred["username"] \
                and data.password == cred["password"]:
            expires_at = datetime.utcnow() + timedelta(hours=1)
            access_token = jwt.encode(
                {"sub": data.username, "exp": expires_at.timestamp()},
                secret, algorithm="HS256"
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": expires_at.timestamp()
            }
    raise HTTPException(
        status_code=400, detail="Incorrect username or password")


def validate_jwt_token(token: str):

    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        exp = payload.get("exp", None)
        if exp is not None and datetime.utcnow() \
                >= datetime.fromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token has expired")
        return payload
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid JWT token")


@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):

    payload = validate_jwt_token(token)
    return {"message": f"Welcome, {payload['sub']}!"}


@app.get("/metatrader5")
async def receive_mql5_call(server: str, account_number: str):

    return {"server": server, "account_number": account_number}
