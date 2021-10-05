#!/bin/sh

echo REGION=$REGION
echo USERPOOLID=$USERPOOLID
echo CLIENTID=$CLIENTID

# 8000ポートをフォワードする
docker run -p 8000:8000 \
	-e REGION=$REGION \
	-e USERPOOLID=$USERPOOLID \
	-e CLIENTID=$CLIENTID \
	-it --rm  cognito-my-sample:last
