# backend/app/core/auth.py

import json, os
from urllib.request import urlopen
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Asegúrate de que estas variables estén cargadas (o vienen de Docker)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = os.getenv("ALGORITHMS", "RS256").split(",")

http_bearer = HTTPBearer()

class TokenPayload(BaseModel):
    sub: str
    scope: str = ""
    permissions: list[str] = []

def get_jwks():
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    return json.loads(jsonurl.read())

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenPayload:
    token = credentials.credentials
    # 1) Decodificar solo la cabecera para leer el "kid"
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Header inválido.")
    if "kid" not in unverified_header:
        raise HTTPException(status_code=401, detail="Token mal formado (sin kid).")
    # 2) Descargar claves públicas de Auth0
    jwks = get_jwks()
    public_key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == unverified_header["kid"]:
            public_key = jwt.construct_rsa_key(jwk)
            break
    if public_key is None:
        raise HTTPException(status_code=401, detail="Clave pública no encontrada.")

    # 3) Verificar firma, issuer y audience
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=f"https://{AUTH0_DOMAIN}/",
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado.")

    # 4) Mapear claims de JWT a nuestro modelo
    token_data = TokenPayload(
        sub=payload.get("sub"),
        scope=payload.get("scope", ""),
        permissions=payload.get("permissions", []),
    )
    return token_data