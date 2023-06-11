import azure.cognitiveservices.speech as speechsdk
import os


class AzureTTS:
    def __init__(self):
        AZURE_API_KEY = os.environ["AZURE_SPEECH_API_KEY"]
        AZURE_REGION = os.environ["AZURE_SPEECH_REGION"]
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_REGION = AZURE_REGION
        self.speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_API_KEY, region=AZURE_REGION
        )
        self.speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_API_KEY, region=AZURE_REGION
        )
        self.audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        # The language of the voice that speaks.
        self.speech_config.speech_synthesis_voice_name = "zh-CN-XiaoyiNeural"
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=self.audio_config
        )

    def text_to_speech_and_play(self, text):
        # Get text from the console and synthesize to the default speaker.
        speech_synthesis_result = self.speech_synthesizer.speak_text_async(text).get()

        if (
            speech_synthesis_result.reason
            == speechsdk.ResultReason.SynthesizingAudioCompleted
        ):
            print("Speech synthesized for text [{}]".format(text))
        elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_synthesis_result.cancellation_details
            print("Speech synthesis canceled:{}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    print(
                        "Error details :{}".format(cancellation_details.error_details)
                    )
                    print("Didy you set the speech resource key and region values?")


if __name__ == "__main__":
    azuretts = AzureTTS()
    azuretts.text_to_speech_and_play("嗯，你好，我是你的智能小伙伴，我的名字叫Cherry，你可以和我畅所欲言，我是很会聊天的哦！")
