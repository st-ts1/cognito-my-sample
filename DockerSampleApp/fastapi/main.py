from typing import Optional
from fastapi import FastAPI, Header, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import os
import sys
import json
import decimal
from jose import JWTError, jwt
import logging
import logging.handlers

import time
import requests
from jose import jwk, jwt
from jose.utils import base64url_decode

logging.basicConfig(
    level=logging.INFO, # info異常でないとpythonの標準ライブラリ等のログがDEBUGで出ている
    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
        "http://192.168.56.103:8080",
        "http://192.168.56.103:8081",
        "http://127.0.0.1:8080",
        ]
app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False, # オリジン間リクエストでCookieをサポートする必要が有るか?
        allow_methods=["*"],
        allow_headers=["*"],
        )

app.mount("/static", StaticFiles(directory="static"), name="static")

# FastAPIのサンプル
@app.get("/")
async def root():
    return {"message": "Hello World v7"}

@app.get("/cog_info")
async def cog_info():
    return {
        "REGION": os.environ.get('REGION', "unknown"),
        "USERPOOLID": os.environ.get('USERPOOLID', "unknown"),
        "CLIENTID": os.environ.get('CLIENTID', "unknown"),
    }

# 参考: https://dev.classmethod.jp/articles/verify_cognit_idtoken_by_apig_custom_auth/
def is_valid_token(token):
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']
    REGION=os.environ.get('REGION', "unknown")
    USERPOOLID=os.environ.get('USERPOOLID', "unknown")
    CLIENTID=os.environ.get('CLIENTID', "unknown")
    keys_url = f'https://cognito-idp.{ REGION }.amazonaws.com/{ USERPOOLID }/.well-known/jwks.json'
    res_cognito = requests.get(keys_url)

    # エンドポイントが見つからなかった場合の処理
    if res_cognito.status_code != 200:
        msg = 'Http request to cognito jwks endpoint failed'
        return {'is_valid_token': False, 'msg': msg, 'claims': None}

    keys = json.loads(res_cognito.text)['keys']

    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    # エンドポイントから公開鍵が見つからなかった場合の処理
    if key_index == -1:
        msg = 'Public key not found in jwks.json'
        return {'is_valid_token': False, 'msg': msg, 'claims': None}

    public_key = jwk.construct(keys[key_index])

    message = str(token).rsplit('.', 1)[0].encode('utf-8')
    encoded_signature = str(token).rsplit('.', 1)[1].encode('utf-8')

    decoded_signature = base64url_decode(encoded_signature)

    # JWTの署名チェックが失敗した場合の処理
    if not public_key.verify(message, decoded_signature):
        msg = 'Signature verification failed'
        return {'is_valid_token': False, 'msg': msg, 'claims': None}

    claims = jwt.get_unverified_claims(token)

    # JWTの有効期限が切れていた場合の処理
    if time.time() > claims['exp']:
        msg = 'Token is expired'
        return {'is_valid_token': False, 'msg': msg, 'claims': None}
    # audクレームが想定された値でない場合の処理
    # CognitoのJWTのaudクレームには、認証されたユーザーで使用されるclient_idが含まれる
    if claims['aud'] not in CLIENTID:
        msg = 'Token was not issued for this audience'
        return {'is_valid_token': False, 'msg': msg, 'claims': None}

    return {'is_valid_token': True, 'msg': 'Signature successfully verified', 'claims': claims}

@app.get('/checkjwt')
def checkjwt(response: Response, imsi:str="", sort:str="desc", to:int=123, limit:int=10, authorization: Optional[str] = Header(None)):
    response.headers["Cache-Control"] = "no-cache, no-store"
    if authorization == None:
        logger.info(f"authorization == None")
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    ret = is_valid_token(authorization)
    if ret.get("is_valid_token") != True:
        # パスワード不一致のため何もしない
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    else:
        claims = ret.get("claims")
        logger.info(f"claims: {claims}")
        return { "ok": True, "claims": claims }