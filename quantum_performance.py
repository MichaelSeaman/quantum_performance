#!/usr/bin/python

import sys
import os
import getopt
import subprocess
from csv_processing import csv_to_tracklist
from csv_processing import getKeySigniture
from rewrite_csv import rewrite_csv
from qsys_interface import QsysInterface

MIDI_INPUT_FILE = "testfiles/Test_midi_waldstein.mid"
INPUT_FILE_PROVIDED = False
OUTPUT_MIDI = False
OUTPUT_MIDI_FILE_NAME = "output.mid"
OUTPUT_WAV = False
OUTPUT_WAV_FILE_NAME = "output.wav"

def main(argv):
    global MIDI_INPUT_FILE
    global INPUT_FILE_PROVIDED
    global OUTPUT_MIDI
    global OUTPUT_WAV_FILE_NAME
    global OUTPUT_WAV
    global OUTPUT_WAV_FILE_NAME

    try:
        opts, args = getopt.getopt(argv, 'i:m:w:', ['input=', 'midiOut=','wavOut='])
        for opt, arg in opts:
            if opt in ('-i','--input'):
                MIDI_INPUT_FILE = arg
                INPUT_FILE_PROVIDED = True
            elif opt in ('-m','--midiOut'):
                OUTPUT_MIDI_FILE_NAME = arg
                OUTPUT_MIDI = True
            elif opt in ('-w','--wavOut'):
                OUTPUT_WAV_FILE_NAME = arg
                OUTPUT_WAV = True
    except getopt.GetoptError as e:
        print("No input provided")
        print(e)

    if(not INPUT_FILE_PROVIDED):
        print("No input file provided. Defaulting to test case.")
    print("Using input midi file: ", MIDI_INPUT_FILE)
    if(not os.path.exists(MIDI_INPUT_FILE)):
        print("File not found")
        sys.exit(0)

    if(OUTPUT_WAV):
        print("Outputing to audio to ", OUTPUT_WAV_FILE_NAME)

    if(OUTPUT_MIDI):
        print("Outputing midi data to ", OUTPUT_MIDI_FILE_NAME)

    if(not OUTPUT_MIDI and not OUTPUT_WAV):
        print("No output selected. Defaulting to audio from console.")
        print("NOTE: If you want to save your performance, Restart and specify")
        print("output by adding -m or -w.  EXAMPLE: ")
        print("$ python quantum_performance.py -i input.mid -w output_wav_file_name.wav")

    # run midi to csv
    midiInputFileName, _ = os.path.splitext(os.path.basename(MIDI_INPUT_FILE))
    csvFileName = os.path.join( os.getcwd(), midiInputFileName + ".csv")

    print("Creating midicsv file at ", csvFileName)
    os.system("midicsv {} {}".format(MIDI_INPUT_FILE, csvFileName))

    # prepping midicsv data for qsys
    rows = open(csvFileName, encoding="latin-1").read().splitlines()
    tracklist = csv_to_tracklist(rows)
    keysig = getKeySigniture(rows)

    #################################################

    # QSYS MAGIC GOES HERE. tracklist SHOULD BE EDITTED

    quantum_translator = QsysInterface(tracklist)
    quantum_translator.run()
    tracklist = quantum_translator.measurements

    #################################################

    # Re-writing csv
    outputCSVLines = rewrite_csv(csvFileName, tracklist)
    with open(csvFileName, 'w') as f:
        f.write("\n".join(outputCSVLines))

    # Writing midi
    if(not OUTPUT_MIDI):
        # I know, I know bad naming of variables....
        outputWavFileName, _ = os.path.splitext(os.path.basename(OUTPUT_WAV_FILE_NAME))
        OUTPUT_MIDI_FILE_NAME = os.path.join( os.getcwd(), outputWavFileName + ".mid")

    print("Creating quanumized midi file at ", OUTPUT_MIDI_FILE_NAME)
    os.system("csvmidi {} {}".format(csvFileName, OUTPUT_MIDI_FILE_NAME))
    os.remove(csvFileName)
    #call Timidity

    if(not OUTPUT_WAV and not OUTPUT_MIDI):
        # If neither option is selected, play wav to console
        os.system("timidity {}".format(OUTPUT_MIDI_FILE_NAME))
        print("Cleaning up.")
        os.remove(OUTPUT_MIDI_FILE_NAME)
    elif(not OUTPUT_WAV and OUTPUT_MIDI):
        pass
    elif(OUTPUT_WAV and not OUTPUT_MIDI):
        print("Creating synthesized wav file at ", OUTPUT_WAV_FILE_NAME)
        os.system("timidity {} -Ow -o {}".format(OUTPUT_MIDI_FILE_NAME, OUTPUT_WAV_FILE_NAME))
        print("Cleaning up.")
        os.remove(OUTPUT_MIDI_FILE_NAME)
    else:
        # Output both
        print("Creating synthesized wav file at ", OUTPUT_WAV_FILE_NAME)
        os.system("timidity {} -Ow -o {}".format(OUTPUT_MIDI_FILE_NAME, OUTPUT_WAV_FILE_NAME))

    print("All done.")


if __name__ == "__main__":
    main(sys.argv[1:])
