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

    csvr = csv.reader(csvfile, delimiter='\t')

    previous_marker = 0
    time_def = 0

    for row in csvr:
        time_def = mido.second2tick(float(row[0]), resolution, tempo) - previous_marker
        track.append(MetaMessage('marker', text=row[2], time=time_def))
        previous_marker = mido.second2tick(float(row[0]), resolution, tempo)

mid.save(
    filedialog.asksaveasfilename(
        filetypes = [('Standard MIDI File', '*.mid')]))