# osint.tool.ongithub
OSINT愛好家の皆さまへ
メアド収集のためにgithubアカウントから、リポジトリのクローンをつくって、ファイルを探して、git logを実行してメアドを見つける
意外と時間がかかりますよね？　それで見つからなかったら悲しいですし、
このツールは別にものすごく役立つわけではないけど時短になります。
git logを実行するまでの時間をコード一行に変換
時間がないあなたへ

インストールが必要なもの
git
python 3.9 以上


使い方（全OS共通）
基本
python gitmailcollect.py クローンURL

TXTに保存
python gitmailcollect.py クローンURL -o emails.txt

JSON出力
python gitmailcollect.py クローンURL --json

noreply除外
python gitmailcollect.py クローンURL --exclude-noreply

期間指定
python gitmailcollect.py クローンURL --since 2024-01-01

ドメインのみ（OSINT研究向け）
python gitmailcollect.py クローンURL --domain-only

コマンド化（任意）
Linux / macOS
chmod +x gitmailcollect.py
mv gitmailcollect.py ~/.local/bin/gitmailcollect
gitmailcollect クローンURL

Windows
python C:\tools\gitmailcollect.py クローンURL


（PATHに入れれば gitmailcollect.py だけでOK）
