# cue2mid
タブ区切りプレーンテキスト (TSV) 形式によるマーカーリストを Standard MIDI File に変換する Python スクリプトです。

入力には iZotope RX や Audacity からエクスポートした TSV ファイルが使えます。<br>
必要に応じて Google スプレッドシートなどを使って調整してからでも構いません。<br>
ソースは 'utf-8' で読み込み、SMF を書き出すときは 'shift_jis' を使います。

## 前提条件
- Python 環境
- [mido](https://mido.readthedocs.io/en/stable/)

mido ってのは Python で MIDI のあれこれをさせてくれる超クールなライブラリーです。<br>
生の MIDI メッセージも 16 進数でガチャガチャできるらしい。しらんけど。

`pip install mido` でインストールしておいてください。<br>
venv? ってやつをしておくとイイカンジになるみたいですよ!<br>
僕は venv さえ初めてだったので PowerShell で activate するだけのために相当時間をかけてしまいました。<br>
(`Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy AllSigned` のこと)

## 使い方
`git clone` するまでもなく cue2mid をおもむろに作業ディレクトリに放り込んで `python cue2mid.py` するだけです。<br>
`tkinter.filedialog` が「開く」ダイアログと「名前を付けて保存」ダイアログを出してくれます。
