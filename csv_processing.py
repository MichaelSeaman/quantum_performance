#!/usr/bin/env python

# Code made possible by shoogle's midicsv-process
# https://github.com/shoogle/midicsv-process


import sys
from midi import *

def csv_to_tracklist(rows):
    tempoMap   = TempoMap()
    notes      = []
    noteEvents = []
    onTicks    = []

    # Reading midi events
    for i, row in enumerate(rows):
        cells = row.split(", ")
        track = int(cells[0])
        tick = int(cells[1])
        rowType = cells[2]
        if rowType == "Header":
            tpqn = int(cells[5]) # set tickcells per quarter note
            tempoMap.tpqn = tpqn
            nTracks = int(cells[4]) + 1
        elif rowType == "Tempo":
            tempo = int(cells[3])
            tempoMap.addTempo(tick, tempo)
        elif rowType in ("Note_on_c","Note_off_c"):
            pitch    = int(cells[4])
            velocity = int(cells[5])
            isNoteOff = (rowType=="Note_off_c" or velocity==0)
            noteEvents.append(NoteEvent(track, tick, pitch, velocity, i, isNoteOff))
        elif rowType == "Key_signature":
            key = int(cells[3])
            tonality = cells[4]

    # Create notes by pairing noteOn and NoteOff events
    for i, noteEvent_i in enumerate(noteEvents):
        if noteEvent_i.isNoteOff:
            continue
        for noteEvent_pair in noteEvents[i:]:
            if ( (not noteEvent_pair.isNoteOff) or
            noteEvent_pair.track != noteEvent_i.track or
            noteEvent_pair.pitch != noteEvent_i.pitch):
                continue
            note = Note(noteEvent_i, noteEvent_pair)
            notes.append(note)
            onTicks.append(note.tick)
            break

    # sort notes by onTick
    notes = [x for (y,x) in sorted(zip(onTicks, notes))]
    onTicks.sort()
    tracklist = [ [] for _ in range(nTracks)]

    # creating tracklist
    for note in notes:
        tracklist[note.track].append([note.octave(), note.pitch % 12,
        note.onTimeMillis(tempoMap) / 1000, 0, note.noteEvent_on.rowNumber,
        note.noteEvent_off.rowNumber ])

    return tracklist

def getKeySigniture(rows):
    for i, row in enumerate(rows):
        cells = row.split(", ")
        track = int(cells[0])
        tick = int(cells[1])
        rowType = cells[2]
        key = 0
        tonality = 0
        if rowType == "Key_signature":
            key = int(cells[3])
            tonality = cells[4]
    return (key, tonality)
