# ビルド環境
FROM node:lts-alpine as build-stage

RUN npm install -g npm && \
npm install -g @vue/cli && \
npm install -g  @vue/cli-init

WORKDIR /vue3-cognito-client
# 先にnpmパッケージをインストールすることでDockerのキャッシュを作る
COPY vue3-cognito-client/package*.json ./
RUN npm install
COPY vue3-cognito-client .
RUN npm run build

# 本番環境
FROM python:3.9.5-slim-buster

# FastAPI関連のpipインストール
RUN pip3 install --no-cache-dir fastapi && \
pip3 install --no-cache-dir "uvicorn[standard]" && \
pip3 install --no-cache-dir python-multipart  && \
pip3 install --no-cache-dir aiofiles && \
pip3 install --no-cache-dir gunicorn && \
pip3 install --no-cache-dir boto3

RUN pip3 install python-jose[cryptography] && \
pip3 install --no-cache-dir requests

# 物理OSのfastapiディレクトリをコンテナ内の/fastapiへコピー
COPY fastapi /fastapi
COPY --from=build-stage /vue3-cognito-client/dist /fastapi/static
# 以降カレントディレクトリが/fastapi
WORKDIR /fastapi

# 公開するport番号
EXPOSE 8000
# apuserを作成
RUN useradd apuser
# プログラムはapuserで実行
USER apuser
# pythonで標準出力のバッファを無効化する環境変数
ENV PYTHONUNBUFFERED 1
# このコンテナで実行するプログラム
#ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0" ]
#ENTRYPOINT [ "gunicorn", "main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000" ]
CMD [ "gunicorn", "main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000" ]
