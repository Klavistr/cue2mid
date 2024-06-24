import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage

mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(60)))
track.append(MetaMessage('marker', text='test', time=0))
track.append(MetaMessage('marker', text='test', time=12))
track.append(MetaMessage('marker', text='test', time=24))
track.append(MetaMessage('marker', text='test', time=36))

mid.save('myfile.mid')