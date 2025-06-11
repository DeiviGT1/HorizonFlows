# app/core/auth.py

import json
import os
from typing import Dict
from urllib.request import urlopen

from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

# Cargar variables de entorno
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("API_AUDIENCE")
ALGORITHMS = os.getenv("ALGORITHMS", "RS256").split(",")

# Define un esquema para leer el header Authorization: Bearer <token>
http_bearer = HTTPBearer()

class TokenPayload(BaseModel):
    sub: str
    scope: str = ""
    permissions: list[str] = []

def get_jwks() -> Dict:
    """Descarga las JWKS (claves públicas) desde Auth0."""
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    return json.loads(jsonurl.read())

def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> TokenPayload:
    token = credentials.credentials
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Header inválido.")
    if "kid" not in unverified_header:
        raise HTTPException(status_code=401, detail="Token mal formado (sin kid).")
    jwks = get_jwks()
    public_key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == unverified_header["kid"]:
            public_key = jwt.construct_rsa_key(jwk)
            break
    if public_key is None:
        raise HTTPException(status_code=401, detail="Clave pública no encontrada.")
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
    # Mapear los claims de JWT a nuestro modelo
    token_data = TokenPayload(
        sub=payload.get("sub"),
        scope=payload.get("scope", ""),
        permissions=payload.get("permissions", []),
    )
    return token_data

def require_permissions(required_scopes: list[str]):
    """Genera un Depends que verifica scopes/permissions específicas."""
    def verifier(token_data: TokenPayload = Security(verify_jwt)):
        token_scopes = token_data.scope.split()
        for scope in required_scopes:
            if scope not in token_scopes:
                raise HTTPException(status_code=403, detail="Permisos insuficientes.")
        return token_data
    return verifier

def require_role(required_role: str):
    """
    Genera una dependencia que verifica si un rol específico existe en el token.
    """
    def verifier(token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> bool:
        # Reutilizamos la lógica de validación del token de verify_jwt
        # pero aquí solo necesitamos el payload decodificado.
        try:
            unverified_header = jwt.get_unverified_header(token.credentials)
            jwks = get_jwks()
            public_key = next((jwt.construct_rsa_key(jwk) for jwk in jwks["keys"] if jwk["kid"] == unverified_header["kid"]), None)
            if public_key is None:
                raise HTTPException(status_code=403, detail="Clave pública no encontrada.")

            payload = jwt.decode(
                token.credentials, public_key, algorithms=ALGORITHMS,
                audience=API_AUDIENCE, issuer=f"https://{AUTH0_DOMAIN}/"
            )
        except JWTError:
            raise HTTPException(status_code=403, detail="Token inválido o expirado.")

        # Buscamos el claim de roles que definimos en la Action de Auth0
        roles = payload.get("https://horizonflows.com/roles", [])

        if required_role not in roles:
            raise HTTPException(status_code=403, detail="Permisos insuficientes. Rol de administrador requerido.")

        return True
    return verifier