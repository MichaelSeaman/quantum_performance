# quantum_performance
Handing midi files to an electron

## Dependencies

* [TiMidiTy](http://timidity.sourceforge.net/)
* [midicsv](http://www.fourmilab.ch/webtools/midicsv/)

## Technical Specification

## Midi to CSV to Midi
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
timidity <YOUR_MIDI_FILE> -Ow
```
An output .wav file will be created in the same directory as your midi file.
