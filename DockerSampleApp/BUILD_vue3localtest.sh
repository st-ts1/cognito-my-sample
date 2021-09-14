#!/bin/sh

# テスト実行、ビルド環境のイメージをビルド
docker build -t vue3localtest:last -f Dockerfilevue3localtest .
