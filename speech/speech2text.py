import os
import azure.cognitiveservices.speech as speechsdk


class AzureASR:
    def __init__(self):
        AZURE_API_KEY = os.environ["AZURE_SPEECH_API_KEY"]
        AZURE_REGION = os.environ["AZURE_SPEECH_REGION"]
        self.AZURE_API_KEY = AZURE_API_KEY
        self.AZURE_REGION = AZURE_REGION
        self.speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_API_KEY, region=AZURE_REGION
        )

    def speech_to_text(self, audio_path: str = "test.wav", if_microphone: bool = True):
        self.speech_config.speech_recognition_language = "zh-CN"
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config, audio_config=audio_config
        )
        print("Speak into your microphone.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized:{}".format(speech_recognition_result.text))
            return speech_recognition_result.text
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print(
                "No speech could be recognized :{}".format(
                    speech_recognition_result.no_match_details
                )
            )
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            print("Speech Recognition canceled:{}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details:{}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
        return None


if __name__ == "__main__":
    azureasr = AzureASR()
    azureasr.speech_to_text()
