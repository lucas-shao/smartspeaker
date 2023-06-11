from wakeword.wakeword import PicoWakeWord
from speech.speech2text import AzureASR
from speech.text2speech import AzureTTS


picowakeword = PicoWakeWord()
print("开始监听唤醒词...")
while True:
    keyword_idx = picowakeword.detect_wake_word()
    if keyword_idx >= 0:
        print("我被唤醒了！")
        AzureTTS().text_to_speech_and_play("主人，人家在的，请讲")
        question = AzureASR().speech_to_text()
        print("你问：{}".format(question))
        answer = question
        print("我答：{}".format(answer))
        AzureTTS().text_to_speech_and_play(answer)
