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