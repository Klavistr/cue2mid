import csv, os
from tkinter import filedialog

import mido
from mido import MidiFile, MidiTrack, MetaMessage

source = filedialog.askopenfilename(
    filetypes = [
        ('Marker List', '*.txt;*.tsv')])

with open(source, encoding='utf-8') as csvfile:
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = mido.bpm2tempo(120)
    resolution = 480

    track.append(MetaMessage('set_tempo', tempo))

    # RX か Audacity かを検出する
    rx_detection = {
        'Time format: Samples': ('Sample', 2),
        'Time format: Time': ('Time', 2),
        'Time format: Timecode': ('Timecode', 3),
        'Time format: Source Time': ('Time', 2),
        'Time format: Source Timecode': ('Timecode', 3),
    }

    whole_txt = csvfile.read().splitlines()

    if whole_txt[1] in rx_detection:
        my_detection = rx_detection[whole_txt[1]]
        div_mode = my_detection[0]
        print('Filetype detected... iZotope RX,', div_mode)
        start_line = my_detection[1]
        if div_mode == 'Sample':
            smpl_rate = input('Sample rate in Hz? ')
        if start_line == 3:
            fps = float(whole_txt[2].replace('Frame rate: ', ''))
            print('Frames per second:', fps)
    else:
        div_mode = 'Audacity Time'
        print('Filetype detected... Audacity')
        start_line = 0
    
with open(source, encoding='utf-8') as csvfile:
    # CSV Reader に読ませる
    csvr = csv.reader(csvfile, delimiter='\t')
    mlist = list(csvr)
    prev = 0

    for i, row in enumerate(mlist):
        if i >= start_line:
            if div_mode == 'Sample':
                sec = row[1] / smpl_rate
                now = mido.second2tick(float(sec), resolution, tempo)
                text = row[0]
            elif div_mode == 'Time':
                hms = row[1].split(':')
                sec = int(hms[0]) * 60 * 60 \
                    + int(hms[1]) * 60 \
                    + float(hms[2])
                now = mido.second2tick(float(sec), resolution, tempo)
                text = row[0]
            elif div_mode == 'Timecode':
                hmsf = row[1].split(':')
                sec = int(hmsf[0]) * 60 * 60 \
                    + int(hmsf[1]) * 60 \
                    + int(hmsf[2]) \
                    + fps / int(hmsf[3])
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

mid.save(
    filedialog.asksaveasfilename(
        defaultextension = 'mid',
        filetypes = [('Standard MIDI File', '*.mid')],
        initialfile = os.path.splitext(os.path.basename(source))[0]))
