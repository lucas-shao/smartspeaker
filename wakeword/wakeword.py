import pvporcupine
import pyaudio
import struct
import os

# 将PICOVOICE_API_KEY需要放入本地环境变量中
PICOVOICE_API_KEY = os.environ["PICOVOICE_API_KEY"]

porcupine = pvporcupine.create(
    access_key=PICOVOICE_API_KEY,
    keyword_paths=["wakeword/Hey-cherry_en_mac_v2_2_0/Hey-cherry_en_mac_v2_2_0.ppn"],
)

myaudio = pyaudio.PyAudio()
stream = myaudio.open(
    input_device_index=0,
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length,
)

print("开始监听唤醒词...")
while True:
    audio_object = stream.read(porcupine.frame_length, exception_on_overflow=False)
    audio_object_unpacked = struct.unpack_from(
        "h" * porcupine.frame_length, audio_object
    )

    keyword_index = porcupine.process(audio_object_unpacked)
    if keyword_index >= 0:
        print("我听到了!")
