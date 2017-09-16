#!/usr/bin/env python

# Code made possible by shoogle's midicsv-process
# https://github.com/shoogle/midicsv-process

# usage:
# python csv_to_tracklist.py <IN_CSV_FILE>

import sys
from midi import *

# TODO: seperate read/writing from the time conversion

if len(sys.argv) <= 1:
    print("Input file needed.")
    sys.exit(0)
else:
    infile = sys.argv[1]

rows = open(infile, encoding="latin-1").read().splitlines()

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
