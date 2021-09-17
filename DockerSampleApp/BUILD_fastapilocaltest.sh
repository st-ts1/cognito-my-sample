#!/bin/sh

# テスト実行、ビルド環境のイメージをビルド
docker build -t fastapilocaltest:last -f Dockerfilefastapilocaltest .
