#!/bin/sh

# 本番環境のイメージをビルド
docker build -t example/cognito-my-sample:v1 -f Dockerfile .
