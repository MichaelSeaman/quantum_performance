#!/usr/bin/env python

def rewrite_csv(csv_in, tracklist):
    rows = open(csv_in, encoding="latin-1").read().splitlines()
    for track in tracklist:
        for measurement in track:
            quantum_note = measurement[3]
            note_on_line_number = measurement[4]
            note_off_line_number = measurement[5]

            for line_number in (note_off_line_number, note_on_line_number):
                row = rows[line_number]
                cells = row.split(", ")
                cells[4] = str(quantum_note)
                rows[line_number] = ', '.join(cells)
    return(rows)
