import csv, os
from tkinter import filedialog

import mido
from mido import MidiFile, MidiTrack, MetaMessage

source = filedialog.askopenfilename(
    filetypes = [
        ('Marker List', '*.txt')])

with open(source, encoding='utf-8') as csvfile:
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(60)
    resolution = 480

    track.append(MetaMessage('set_tempo', tempo))

    # 2024.6.26 現在、Audacity のみに対応
    # iZotope RX は先頭 2 行で時分秒表記かタイムコード表記かを区別するうえ
    # マーカー名 → 開始位置 → 終了位置に並ぶのでそれをなんかイイカンジにする
    csvr = csv.reader(csvfile, delimiter='\t')

    prev_marker = 0
    time_def = 0

    # RX 対応のため row[n] を入れ替えられるようにしたい
    for row in csvr:
        time_def = mido.second2tick(float(row[0]), resolution, tempo) - prev_marker
        track.append(MetaMessage('marker', text=row[2], time=time_def))
        prev_marker = mido.second2tick(float(row[0]), resolution, tempo)

mid.save(
    filedialog.asksaveasfilename(
        filetypes = [('Standard MIDI File', '*.mid')]))