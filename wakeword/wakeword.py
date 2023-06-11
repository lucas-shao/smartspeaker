import pvporcupine
import pyaudio
import struct
import os


class PicoWakeWord:
    def __init__(self):
        # 将PICOVOICE_API_KEY需要放入本地环境变量中
        PICOVOICE_API_KEY = os.environ["PICOVOICE_API_KEY"]
        self.porcupine = pvporcupine.create(
            access_key=PICOVOICE_API_KEY,
            keyword_paths=[
                "wakeword/Hey-cherry_en_mac_v2_2_0/Hey-cherry_en_mac_v2_2_0.ppn"
            ],
        )
        self.myaudio = pyaudio.PyAudio()
        self.stream = self.myaudio.open(
            input_device_index=0,
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )

    def detect_wake_word(self):
        audio_obj = self.stream.read(
            self.porcupine.frame_length, exception_on_overflow=False
        )
        audio_obj_unpacked = struct.unpack_from(
            "h" * self.porcupine.frame_length, audio_obj
        )
        keyword_idx = self.porcupine.process(audio_obj_unpacked)
        return keyword_idx


if __name__ == "__main__":
    picowakeword = PicoWakeWord()
    print("开始监听唤醒词...")
    while True:
        keyword_idx = picowakeword.detect_wake_word()
        if keyword_idx >= 0:
            print("我听到了！")
