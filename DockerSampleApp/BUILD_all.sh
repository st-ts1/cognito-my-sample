#!/bin/sh

# テスト実行、ビルド環境のイメージをビルド
docker build -t cognito-my-sample:last -f Dockerfile .