import wave
import sys
import pyaudio
# from audio import play_audio, testaudio

import struct
import time
    
def extrac_header_data(header_data):

    # Specify the binary data of the first 44 bytes
    # header_data = b'RIFF....'  # Replace with your actual 44 bytes of data

    # Unpack the binary data to extract header information
    chunk_id = header_data[0:4].decode('ascii')
    chunk_size = struct.unpack('<I', header_data[4:8])[0]
    format = header_data[8:12].decode('ascii')
    subchunk1_id = header_data[12:16].decode('ascii')
    subchunk1_size = struct.unpack('<I', header_data[16:20])[0]
    audio_format = struct.unpack('<H', header_data[20:22])[0]
    num_channels = struct.unpack('<H', header_data[22:24])[0]
    sample_rate = struct.unpack('<I', header_data[24:28])[0]
    byte_rate = struct.unpack('<I', header_data[28:32])[0]
    block_align = struct.unpack('<H', header_data[32:34])[0]
    bits_per_sample = struct.unpack('<H', header_data[34:36])[0]
    subchunk2_id = header_data[36:40].decode('ascii')
    subchunk2_size = struct.unpack('<I', header_data[40:44])[0]

    # Print the extracted header information
    print("Chunk ID:", chunk_id)
    print("Chunk Size:", chunk_size)
    print("Format:", format)
    print("Subchunk1 ID:", subchunk1_id)
    print("Subchunk1 Size:", subchunk1_size)
    print("Audio Format:", audio_format)
    print("Num Channels:", num_channels)
    print("Sample Rate:", sample_rate)
    print("Byte Rate:", byte_rate)
    print("Block Align:", block_align)
    print("Bits per Sample:", bits_per_sample)
    print("Subchunk2 ID:", subchunk2_id)
    print("Subchunk2 Size:", subchunk2_size)


stream_parameters = {
    # 'rate': 44100,
    'rate':22050,
    'channels': 1,
    # 'format': 2,
    'output': True,
    # 'frames_per_buffer': 1024
}

def play_audio(generator):
    p = pyaudio.PyAudio()
    # pyaudio.
    stream_parameters["format"] = p.get_format_from_width(2)
    print(stream_parameters)
    stream = p.open(**stream_parameters)
    # stream = p.open()
    for data in generator:
        stream.write(data)
    stream.close()
    p.terminate()

def testaudio():
    def gen():
        with open('/home/ubuntu/Music/vi.wav', 'rb') as wf:
            while True:
                x = wf.read(1024)
                # time.sleep()
                
                # print(x, len(x))
                # extrac_header_data(x)
                # return 
                if len(x)==0: return 
                # print(len(x))
                yield x
        
        # with wave.open("/home/ubuntu/Music/vi.wav", 'rb') as wf:
        #     x =  wf.readframes(1024)
        #     print(26, len(x))
        # print(27, 'close')
    play_audio(gen())

if __name__ == "__main__":
    testaudio()


