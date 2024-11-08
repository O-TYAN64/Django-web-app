# Django-web-app

## 使用環境（サーバー側)
Ubuntu22.04 LTS <br>
Windows11

## テスト環境 (Web閲覧側)
iOS 18 <br>
Android 13 <br>
Windows11<br>
Safari <br>
Chrome 130 <br>
Firefoz 131 <br>

## 使用言語
python 3.11<br>
javascript<br>
css<br>
html<br>


# 環境構築
## ライブラリーインストール
`pip3 install -r requirements.txt`<br>

# Djangoの使い方
## マイグレーションする内容を一覧表示
マイグレーションファイルを作成する前にマイグレーション内容を確認したい時に使用<br>
`python3 manage.py makemigrations`
## マイグレーションファイルを作成
マイグレーションファイルを作成<br>
`python3 manage.py migrate`
## マイグレーションファイルをデータベースに適用
作成したマイグレーションファイルをデータベースに適用<bR>
`python manage.py createsuperuser`
## Djangoプロジェクトを起動
Djangoプロジェクトをローカル環境で起動する時に使用します。<br>
[アドレス/ポート番号]には、好きなポート番号を指定できる。<br>
未入力の場合は、自動的に8000番ポートになります。<br>
`python manage.py runserver [アドレス/ポート番号]`
