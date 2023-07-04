https://api.python.langchain.com/en/latest/modules/embeddings.html


For ubuntu 18.04 just install ffmpeg

sudo apt install ffmpeg

pydub:
RuntimeWarning: Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
  warn("Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work", RuntimeWarning)

vi.wav

Chunk ID: RIFF
Chunk Size: 36
Format: WAVE
Subchunk1 ID: fmt 
Subchunk1 Size: 16
Audio Format: 1
Num Channels: 1
Sample Rate: 22050
Byte Rate: 44100
Block Align: 2
Bits per Sample: 16
Subchunk2 ID: data
Subchunk2 Size: 268435456


en.wav (currently not working)

Chunk ID: RIFF
Chunk Size: 115963
Format: WAVE
Subchunk1 ID: fmt 
Subchunk1 Size: 18
Audio Format: 7
Num Channels: 1
Sample Rate: 24000
Byte Rate: 24000
Block Align: 1
Bits per Sample: 8
Subchunk2 ID: fa
Subchunk2 Size: 291939


python copy generator
generator
threading generator