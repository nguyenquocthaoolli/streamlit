# import sys
# import pyaudio

# import struct
# import multiprocessing

# def queueToGenerator(q: multiprocessing.Queue):
#     while True:
#         v = q.get()
#         if v is None: return
#         yield v
    
# def extrac_header_data(header_data):

#     # Specify the binary data of the first 44 bytes
#     # header_data = b'RIFF....'  # Replace with your actual 44 bytes of data

#     # Unpack the binary data to extract header information
#     chunk_id = header_data[0:4].decode('ascii')
#     chunk_size = struct.unpack('<I', header_data[4:8])[0]
#     format = header_data[8:12].decode('ascii')
#     subchunk1_id = header_data[12:16].decode('ascii')
#     subchunk1_size = struct.unpack('<I', header_data[16:20])[0]
#     audio_format = struct.unpack('<H', header_data[20:22])[0]
#     num_channels = struct.unpack('<H', header_data[22:24])[0]
#     sample_rate = struct.unpack('<I', header_data[24:28])[0]
#     byte_rate = struct.unpack('<I', header_data[28:32])[0]
#     block_align = struct.unpack('<H', header_data[32:34])[0]
#     bits_per_sample = struct.unpack('<H', header_data[34:36])[0]
#     subchunk2_id = header_data[36:40].decode('ascii')
#     subchunk2_size = struct.unpack('<I', header_data[40:44])[0]

#     # Print the extracted header information
#     print("Chunk ID:", chunk_id)
#     print("Chunk Size:", chunk_size)
#     print("Format:", format)
#     print("Subchunk1 ID:", subchunk1_id)
#     print("Subchunk1 Size:", subchunk1_size)
#     print("Audio Format:", audio_format)
#     print("Num Channels:", num_channels)
#     print("Sample Rate:", sample_rate)
#     print("Byte Rate:", byte_rate)
#     print("Block Align:", block_align)
#     print("Bits per Sample:", bits_per_sample)
#     print("Subchunk2 ID:", subchunk2_id)
#     print("Subchunk2 Size:", subchunk2_size)

#     return {
#         "rate": sample_rate,
#         "channels": num_channels,
#         "format": pyaudio.get_format_from_width(bits_per_sample/8)
#     }


# def play_audio(generator):
#     p = pyaudio.PyAudio()
#     stream = None
#     for data in generator:
#         if not stream:
#             stream_parameters = extrac_header_data(data)
#             # stream_parameters["format"]=128
#             # print(stream_parameters)
#             stream = p.open(**stream_parameters, output=True, frames_per_buffer=1024)
#         # print(65, len(data))
#         stream.write(data)
#     stream.close()
#     p.terminate()

# def testaudio():
#     fn = '/home/ubuntu/olli/nodejs/output.ogg'
#     # fn = '/home/ubuntu/Music/enstream.wav'
#     def gen():
#         with open(fn, 'rb') as wf:
#             while True:
#                 x = wf.read(1024)
#                 if len(x)==0: return 
#                 yield x
        
#     play_audio(gen())

# if __name__ == "__main__":
#     testaudio()


