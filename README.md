# quantum_performance
Handing midi files to an electron

## What's going on?

Aaron, this is where you're the expert.

# Temp
Run webserver with:
```
FLASK_APP=server.py flask run
```


## Dependencies

To get started, quantum performance will need the following command line
 programs installed:

* [TiMidiTy](http://timidity.sourceforge.net/)
* [midicsv](http://www.fourmilab.ch/webtools/midicsv/)

Also, make sure that python3 is installed on your machine

## Usage

Run the quantum simulation with
```
python3 quantum_performance.py -i INPUTFILE.mid -w OUTPUT_WAV_FILE.wav -m OUTPUT_WAV_FILE.mid
```
The created midi or wav files should be in the directory you ran the program from.
The '-w' argument specifies the outputted .wav audio file, and the '-m' specifies
the outputted .mid file. If both are omitted, then audio will just play from
the host shell.


## Technical Specification

### Midi to CSV to Midi
Conversion will be done with [midicsv](http://www.fourmilab.ch/webtools/midicsv/#Download)
Luckily this is on brew!
```
#MAC OSX
brew install midicsv
```
Run with the following command
```
midicsv <IN_MIDI_FILE> <OUT_CSV_FILE>

```
Or to travel the other way:
```
csvmidi <IN_CSV_FILE> <OUT_MIDI_FILE>
```

### Midi to Audio
Conversion will be done with Timidity
```
# MAC OSX
brew install timidity

# OR on Linux
apt-get install timidity
```
Once ready, you can synthesize sounds from midi files by doing:
```
timidity <YOUR_MIDI_FILE> -Ow -o <OUTFILE>
```
An output .wav file will be created in the same directory as your midi file.


## Authors
* **Michael Seaman** - [Github](https://github.com/michaelseaman)
* **Aaron Grisez** - [Qhord](https://www.qhord.com/)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.
