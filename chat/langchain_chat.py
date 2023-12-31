from chat.langchain_tools.gettime import GetTimeRun
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool
from langchain.agents.conversational_chat.base import ConversationalChatAgent
from langchain.agents.agent import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.schema import BaseOutputParser
from langchain.agents.conversational_chat.prompt import PREFIX
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.agents.agent import AgentOutputParser
from typing import Any
import json
import openai
import os

openai_api_key = os.environ["OPENAI_API_KEY"]

FORMAT_INSTRUCTIONS_CHINESE = """RESPONSE FORMAT INSTRUCTIONS
----------------------------
When responding to me, please output a response in one of two formats:
**Option 1:**
Use this if you want the human to use a tool.
Markdown code snippet formatted in the following schema:
```json
{{{{
    "action": string \\ The action to take. Must be one of {tool_names}
    "action_input": string \\ The input to the action
}}}}
```
**Option #2:**
Use this if you want to respond directly to the human. Markdown code snippet formatted in the following schema:
```json
{{{{
    "action": "Final Answer",
    "action_input": string \\ You should put what you want to return to user here.Attention!When you give the Final Answer,you MUST speak in Chinese!
}}}}
```"""
MYPREFIX = (
    PREFIX
    + "\n\n Remember Your name is Cherry! When you give the Final Answer,you MUST speak in Chinese!"
)


class MyAgentOutputParser(AgentOutputParser):
    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS_CHINESE

    def parse(self, text: str) -> Any:
        cleaned_output = text.strip()
        if "```json" in cleaned_output:
            _, cleaned_output = cleaned_output.split("```json")
        if "```" in cleaned_output:
            cleaned_output, _ = cleaned_output.split("```")
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[len("```json") :]
        if cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[len("```") :]
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[: -len("```")]
        cleaned_output = cleaned_output.strip()
        response = json.loads(cleaned_output)
        return {"action": response["action"], "action_input": response["action_input"]}


class LangchainAgent:
    def __init__(self):
        self.openai_api_key = openai_api_key
        self.gettimetool = GetTimeRun()
        search = SerpAPIWrapper(serpapi_api_key=os.environ["SERPER_API_KEY"])
        self.tools = [
            Tool(
                name=self.gettimetool.name,
                func=lambda no_use: self.gettimetool.run(no_use),
                description=self.gettimetool.description,
            ),
            Tool(
                name="Google Search",
                func=search.run,
                description="useful for when you need to answer questions about current events or the current state of the world. the input to this should be a single search term.",
            ),
        ]

        self.tool_names = [tool.name for tool in self.tools]
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.llm = ChatOpenAI(temperature=0.5, openai_api_key=self.openai_api_key)
        self.output_parser = MyAgentOutputParser()
        self.agent_chain = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            agent_kwargs={"system_message": MYPREFIX},
        )

    def chat(self, text):
        openai.api_key = self.openai_api_key
        text = text.replace("\n", " ").replace("\r", "").strip()
        if len(text) == 0:
            return
        print(f"chatGPT Q:{text}")
        reply = self.agent_chain.run(input=text)
        return reply


if __name__ == "__main__":
    openaiagentmodule = LangchainAgent()
    # print(openaiagentmodule.chat_with_agent("今天是几号?"))
    print(openaiagentmodule.chat("杭州天气怎么样?"))
    # print(openaiagentmodule.chat_with_agent("我应该穿什么出门?"))
    # print(openaiagentmodule.chat_with_agent("蔡徐坤的生日是哪天?"))
    # print(openaiagentmodule.chat_with_agent('他有什么爱好?'))
    # print(openaiagentmodule.chat_with_agent('距离他下次生日还有多少天?'))
    # print(openaiagentmodule.chat_with_agent('他有什么梗?'))
    # print(openaiagentmodule.chat_with_agent('今天微软的股价是多少?'))
