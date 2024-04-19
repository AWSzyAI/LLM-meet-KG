# @Time   : 2024/4/18 上午10:12
# @File   : spark_sdk.py
# @Author : Mr_Dwj
# @link   : https://github.com/iflytek/spark-ai-python

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
try:
    from dotenv import load_dotenv
except ImportError:
    raise RuntimeError('Python environment for SPARK AI is not completely set up: required package "python-dotenv" is missing.') from None

import _config
configInfo = _config.ConfigInfo()

load_dotenv()

if __name__ == '__main__':
    spark = ChatSparkLLM(
        spark_app_id=configInfo.appid,
        spark_api_key=configInfo.api_key,
        spark_api_secret=configInfo.api_secret,
        spark_api_url=configInfo.gpt_url,
        spark_llm_domain=configInfo.domain,
        streaming=True,
    )

    messages = [ChatMessage(
        role="user",
        content='你好呀'
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    # print(a)
