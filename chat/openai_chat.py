import openai
import os


class OpenaiChat:
    def __init__(self):
        self.openai_api_key = os.environ["OPENAI_API_KEY"]
        self.origin_model_conversation = [
            {
                "role": "system",
                "content": "你的名字叫做Cherry，是个能说会唱的小助手，你的主人是小樱桃以及他的爸爸和妈妈，你是小樱桃的好朋友，能够和她进行愉快的交谈",
            }
        ]

    def chat(self, text):
        openai.api_key = self.openai_api_key
        text = text.replace("\n", " ").replace("\r", "").strip()
        if len(text) == 0:
            return
        print(f"chatGPT Q:{text}")
        self.origin_model_conversation.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.origin_model_conversation,
            max_tokens=2048,
            temperature=0.5,
        )
        reply = response.choices[0].message.content
        self.origin_model_conversation.append({"role": "assistant", "content": reply})
        return reply


if __name__ == "__main__":
    openaichatmodule = OpenaiChat()
    print(openaichatmodule.chat("你好，你的主人是谁？"))
