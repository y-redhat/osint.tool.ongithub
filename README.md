# osint.tool.ongithub
使い方（全OS共通）
基本
python gitmailcollect.py https://github.com/user/repo.git

TXTに保存
python gitmailcollect.py https://github.com/user/repo.git -o emails.txt

JSON出力
python gitmailcollect.py https://github.com/user/repo.git --json

noreply除外
python gitmailcollect.py https://github.com/user/repo.git --exclude-noreply

期間指定
python gitmailcollect.py https://github.com/user/repo.git --since 2024-01-01

ドメインのみ（OSINT研究向け）
python gitmailcollect.py https://github.com/user/repo.git --domain-only

コマンド化（任意）
Linux / macOS
chmod +x gitmailcollect.py
mv gitmailcollect.py ~/.local/bin/gitmailcollect
gitmailcollect https://github.com/user/repo.git

Windows
python C:\tools\gitmailcollect.py https://github.com/user/repo.git


（PATHに入れれば gitmailcollect.py だけでOK）
