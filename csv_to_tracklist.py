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
            nTracks = int(cells[4])
        elif rowType == "Tempo":
            tempo = int(cells[3])
            tempoMap.addTempo(tick, tempo)
        elif rowType == "Note_on_c":
            pitch    = int(cells[4])
            velocity = int(cells[5])
            noteEvents.append(NoteEvent(track, tick, pitch, velocity, i))

    # Create notes by pairing noteOn and NoteOff events
    for i, noteEvent_on in enumerate(noteEvents):
        if noteEvent_on.velocity ==0:
            continue
        for noteEvent_off in noteEvents[i:]:
            if (noteEvent_off.velocity != 0 or
            noteEvent_off.track != noteEvent_on.track or
            noteEvent_off.pitch != noteEvent_on.pitch):
                continue
            note = Note(noteEvent_on, noteEvent_off)
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
