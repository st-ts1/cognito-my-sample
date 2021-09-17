#!/bin/sh


echo REGION=$REGION
echo USERPOOLID=$USERPOOLID
echo CLIENTID=$CLIENTID

# テスト実行、ビルド環境のイメージを実行
# カレントディレクトリ直下のfastapiをコンテナに見せる。
# 8000ポートをフォワードする
docker run -v `pwd`/fastapi:/fastapi -p 8000:8000 \
	-e REGION=$REGION \
	-e USERPOOLID=$USERPOOLID \
	-e CLIENTID=$CLIENTID \
	-it --rm  fastapilocaltest:last /bin/sh
