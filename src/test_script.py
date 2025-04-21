# from zhipuai import ZhipuAI
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
PLANETZERO_API_KEY = os.environ.get("PLANETZERO_API_KEY")
PLANETZERO_API_BASE = os.environ.get("PLANETZERO_API_BASE")
# from openai import DefaultHttpxClient
# import httpx
newclient = None


def run_llm(prompt, temperature=0.1, engine="gpt-4-turbo"):
    messages = [{"role": "system", "content": "You are an AI assistant that helps people find information."}]
    message_prompt = {"role": "user", "content": prompt}
    messages.append(message_prompt)
    global newclient
    if newclient is None:
        if "llama" in engine.lower():
            newclient = OpenAI(
                api_key='EMPTY',
                base_url=PLANETZERO_API_BASE
            )
        elif "gpt" in engine.lower():
            newclient = OpenAI(
                api_key=PLANETZERO_API_KEY,
                base_url=PLANETZERO_API_BASE,
            )
        elif 'glm' in engine.lower():
            newclient = OpenAI(
                api_key=PLANETZERO_API_KEY,
                base_url="https://open.bigmodel.cn/api/paas/v4/")
    f = 0
    while (f == 0):
        try:
            completion = newclient.chat.completions.create(
                model=engine,
                messages=messages,
                temperature=temperature,
            )
            # print(completion)
            result = completion.choices[0].message.content
            f = 1
        except Exception as e:
            print(e)
            print(engine + " error, retry")
            time.sleep(2)
    
    return result


if __name__ == '__main__':
    prompt = 'Hello World'
    print(run_llm(prompt, engine="gpt-4-turbo"))
