#!/bin/sh

# テスト実行、ビルド環境のイメージを実行
# カレントディレクトリ直下のvue-fastapi_raspberryをコンテナに見せる。
# 8081ポートをフォワードする
docker run -v `pwd`/vue3-cognito-client:/vue3-cognito-client -p 8081:8080 -it --rm  vue3localtest:last /bin/sh
