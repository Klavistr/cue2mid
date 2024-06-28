import csv, os
from tkinter import filedialog

import mido
from mido import MidiFile, MidiTrack, MetaMessage

# 開くファイルはタブ区切りプレーンテキストである必要がある
source = filedialog.askopenfilename(
    filetypes = [
        ('Marker List', '*.txt;*.tsv')])

# MidiFile クラスのインスタンスを作るときに文字コードを指定できる
# 日本語環境なら 'shift_jis' にすること
mid = MidiFile(charset='shift_jis')

# Track クラスのインスタンスを作成し、MidiFile に追加する
track = MidiTrack()
mid.tracks.append(track)

# ここは使っている DAW ソフトや作業するプロジェクトによって変えてもよい
tempo = mido.bpm2tempo(120)
resolution = 480

# テンポ情報を MetaMessage クラスのインスタンスとして Track に追加する
track.append(MetaMessage('set_tempo', tempo))

# RX 検出用の辞書を用意しておく
rx_detection = {
    'Time format: Samples': ('RX Sample', 2),
    'Time format: Time': ('RX Time', 2),
    'Time format: Timecode': ('RX Timecode', 3),
    'Time format: Source Time': ('RX Time', 2),
    'Time format: Source Timecode': ('RX Timecode', 3),
}

# 2 回のファイル読み書きにわたり使う変数なのでここで準備
div_mode = ''

# RX か Audacity かを検出するために一度ファイルを開く
with open(source, encoding='utf-8') as csvfile:
    # とりあえず全行読んでしまう
    whole_txt = csvfile.read().splitlines()

    # もし iZotope RX 仕様なら 2 行目で判断できる
    # (1 行目は読んだところで Marker file version: 1 としか書いていない)
    if whole_txt[1] in rx_detection:
        # ファイル 2 行目と一致するものを辞書の key から探して
        my_detection = rx_detection[whole_txt[1]]

        # 辞書の value[0] を分割モード
        div_mode = my_detection[0]
        print('Filetype detected...', div_mode)

        # 辞書の value[1] を開始行としてそれぞれ取り込む
        start_line = my_detection[1]

        if div_mode == 'RX Sample':
            # サンプルレートの情報は埋め込まれていないので
            # 44100 とか 192000 とか手打ちする必要がある
            smpl_rate = int(input('Sample rate in Hz? '))
        if div_mode == 'RX Timecode':
            # フレームレートはちゃんと書かれているので拾ってきて変数に格納する
            fps = float(whole_txt[2].replace('Frame rate: ', ''))
            print('Frames rate:', fps)
    else:
        # ここまでの条件で何も引っかからなかったら Audacity 仕様と判断する
        print('Filetype detected... Audacity')
        start_line = 0

# CSV Reader に読ませる
with open(source, encoding='utf-8') as csvfile:
    csvr = csv.reader(csvfile, delimiter='\t')
    rows = list(csvr)
    prev = 0

    for i, row in enumerate(rows):
        if i < start_line:
            # 開始行に達していないうちはスキップ
            print('* Skipped: row', i)
        else:
            # 分割モードによってパラメーターを用意する
            if div_mode == 'RX Sample':
                sec = int(row[1]) / smpl_rate
                now = mido.second2tick(float(sec), resolution, tempo)
                text = row[0]
            elif div_mode == 'RX Time':
                hms = row[1].split(':')
                sec = int(hms[0]) * 60 * 60 \
                    + int(hms[1]) * 60 \
                    + float(hms[2])
                now = mido.second2tick(float(sec), resolution, tempo)
                text = row[0]
            elif div_mode == 'RX Timecode':
                hmsf = row[1].split(':')
                sec = int(hmsf[0]) * 60 * 60 \
                    + int(hmsf[1]) * 60 \
                    + int(hmsf[2]) \
                    + fps / float(hmsf[3])
                now = mido.second2tick(float(sec), resolution, tempo)
                text = row[0]
            else:
                # Audacity
                sec = row[0]
                now = mido.second2tick(float(sec), resolution, tempo)
                text = row[2]

            time = now - prev
            track.append(MetaMessage('marker', text=text, time=time))
            print('->', sec, text)
            prev = now

# MIDI ファイルを保存する
mid.save(
    filedialog.asksaveasfilename(
        defaultextension = 'mid',
        filetypes = [('Standard MIDI File', '*.mid')],
        initialfile = os.path.splitext(os.path.basename(source))[0]))