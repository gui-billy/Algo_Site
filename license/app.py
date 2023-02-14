import secrets
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException
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
    '''
    A rota /login é usada para autenticar um usuário fornecendo um nome de usuário e uma senha. 
    Se as credenciais são válidas, um token JWT é gerado e retornado para o cliente. 
    Caso contrário, uma exceção HTTP é lançada.
    '''
    for cred in CREDENTIALS:
        if data.username == cred["username"] and data.password == cred["password"]:
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
    ''''
    A função validate_jwt_token é usada para validar o token JWT fornecido pelo cliente. 
    Ele verifica se o token está codificado com a chave secreta correta e se o tempo de expiração do token não foi ultrapassado.
    '''
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        exp = payload.get("exp", None)
        if exp is not None and datetime.utcnow() >= datetime.fromtimestamp(exp):
            raise HTTPException(status_code=401, detail="Token has expired")
        return payload
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid JWT token")


@app.get("/protected")
async def protected(token: str = Depends(oauth2_scheme)):
    '''
    A rota /protected é protegida pelo esquema de segurança OAuth2PasswordBearer e somente é acessível se um token JWT válido for fornecido com a solicitação. 
    A função validate_jwt_token é usada para validar o token e retornar uma mensagem de boas-vindas para o usuário.
    '''
    payload = validate_jwt_token(token)
    return {"message": f"Welcome, {payload['sub']}!"}


@app.get("/metatrader5")
async def receive_mql5_call(server: str, account_number: str):
    '''
    A rota "/metatrader5" é pública. 
    Quando a plataforma faz uma chamada para o servidor, essa rota é acionada e recebe dois parâmetros, "server" e "account_number". 
    Esses parâmetros são imprimidos para fins de depuração e permitem identificar de forma única a conta de negociação que está sendo acessada na plataforma MetaTrader 5.
    '''
    # return {"server": server, "account_number": account_number}
    return "py-ok"
