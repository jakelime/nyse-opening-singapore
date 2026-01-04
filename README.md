# nyse-opening-singapore

Plays the NYSE opening bell on your computer every market opening day. Automatically detects if it is a weekend or market holiday.

## Tools

### Running the audio tools

Download the NYSE opening bell free from [audio.com](https://audio.com/timbretinkermaster/audio/new-york-stock-exchange-bell).

The script `edit_sound.py` will edit specifically this 20s audio file to 10s.

```bash
brew install ffmpeg
brew install portaudio
pip install -r requirements.txt
python edit_sound.py
```
