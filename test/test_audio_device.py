import pyaudio

p = pyaudio.PyAudio()

# 可以详细罗列出所有音频设备的index，通道数等信息
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(info)
