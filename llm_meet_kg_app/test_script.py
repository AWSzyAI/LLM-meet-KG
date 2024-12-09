import json
from openai import OpenAI
# from zhipuai import ZhipuAI
import time

from openai import OpenAI
# from openai import DefaultHttpxClient
# import httpx
newclient = None

api_keys = 'sk-qQx4nU8nidLUR61hKpFJgFZu6ATMwcVpT1pGJmv40nTVoI2N'
api_base = 'https://api.planetzero.live/v1/'


def run_llm( prompt, temperature=0.1, engine="gpt-4-turbo"):
    messages = [{"role":"system","content":"You are an AI assistant that helps people find information."}]
    message_prompt = {"role":"user","content":prompt}
    messages.append(message_prompt)
    global newclient
    if newclient is None:
        if "llama" in engine.lower():
            newclient = OpenAI(
                api_key='EMPTY',
                base_url=api_base
            )
        elif "gpt" in engine.lower():
            newclient = OpenAI(
                api_key=api_keys,
                base_url=api_base,
            )
        elif 'glm' in engine.lower():
            newclient = OpenAI(
                api_key=api_keys,
                base_url="https://open.bigmodel.cn/api/paas/v4/")
    f = 0
    while(f == 0):
        try:
            completion = newclient.chat.completions.create(
                model=engine,
                messages = messages,
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
    print(run_llm( prompt, engine="gpt-4-turbo"))


