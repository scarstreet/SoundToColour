import colorsys
import librosa
import librosa.display
import scipy as sp
import IPython.display as ipd
import matplotlib.pyplot as plt
import numpy as np
import statistics as s
import math

NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def note2hue(note, noteList, rtrn="hexa"):
    index = -1
    if('#' in note):
        index = noteList.index(note[:2])
    else:
        index = noteList.index(note[0])
    hue = (index/12)
    rgb = colorsys.hsv_to_rgb(hue, 0.9, 0.8)
    rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
    rgb = (math.floor(rgb[0]), math.floor(rgb[1]), math.floor(rgb[2]))
    if(rtrn == 'rgb'):
        return rgb
    hexa = '#%02x%02x%02x' % rgb  # how to get hexadecimal from rgb
    return hexa

def allNote2Hue(allMidi, noteList):
    allNote = []
    for m in allMidi:
        temp = m
        try:
            temp['colour'] = note2hue(m['midi'], noteList, rtrn='hexa')
        except:
            temp['colour'] = '-'
        allNote.append(temp)
    return allNote

def midi2hue(midi, amp, maxAmp, rtrn="hexa"):
    hue = (midi % 12)/12
    val = 0.70+(midi/96)*0.30
    sat = 0.70-(midi/96)*0.30
    
    ampp = 0.20 * amp/maxAmp
    sat -= ampp
    val += ampp
    val = 1 if val > 1 else val

    rgb = colorsys.hsv_to_rgb(hue, sat, val)
    rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
    rgb = (math.floor(rgb[0]), math.floor(rgb[1]), math.floor(rgb[2]))
    if(rtrn == 'rgb'):
        return rgb
    hexa = '#%02x%02x%02x' % rgb
    return hexa

def allMidi2Hue(allMidi):
    allNote = []
    maxAmp = max(allMidi, key=lambda x: x['amp'])['amp']
    for m in allMidi:
        temp = m
        try:
            temp['colour'] = midi2hue(m['midi'], m['amp'], maxAmp)
        except:
            temp['colour'] = '-'
        allNote.append(temp)
    return allNote

def getTempo(song, sr):
    onset_env = librosa.onset.onset_strength(y=song, sr=sr)
    tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
    return tempo

def secondsPerBeat(tempo):
    secPerBeat = 60 / tempo
    return secPerBeat

def getFreq(signal, sr):
    ft = sp.fft.fft(signal)
    magnitude = np.absolute(ft)
    freq = np.linspace(0, sr, len(magnitude))
    return freq, magnitude

def getRms(song, spb):
    FRAME_LEN = spb*2
    HOP_LEN = spb

    rms = librosa.feature.rms(
        song, frame_length=FRAME_LEN, hop_length=HOP_LEN)[0]

    return rms

def getMidi(magnitude):
    index = np.argmax(magnitude)
    try:
        midi = librosa.hz_to_midi(index)
    except:
        midi = '-'
    return midi

def getMidiAll(signal, sr, spb):
    songDuration = len(signal)
    samplePerBeat = math.ceil(spb*sr)
    rms = getRms(signal, samplePerBeat)
    allMidi = []
    for p in range(0, songDuration, samplePerBeat):
        oneBeat = []
        if(p+samplePerBeat < songDuration):
            oneBeat = signal[p:p+samplePerBeat]
        else:
            oneBeat = signal[p:]
        freq, magnitude = getFreq(oneBeat, sr)
        midi = getMidi(magnitude)
        allMidi.append({'start': round((p)*(1/sr), 2),
                       'end': round((p+samplePerBeat)*(1/sr), 2), 'midi': midi})
    for i in range(len(allMidi)):
        allMidi[i]['amp'] = rms[i]
    return allMidi

def getAllMidi(song, sr):
    tempo = getTempo(song, sr)
    spb = secondsPerBeat(tempo)
    allMidi = getMidiAll(song, sr, spb)
    allMidi = allMidi2Hue(allMidi)
    return allMidi

def soundToColor(songPath):
    song_path = songPath
    song, sr = librosa.load(song_path)
    allMidi = getAllMidi(song, sr)
    return allMidi
