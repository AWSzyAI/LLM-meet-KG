import csv
import os

from dotenv import load_dotenv
from openai import ChatCompletion
from openai import OpenAI

load_dotenv()
PLANETZERO_API_KEY = os.environ.get("PLANETZERO_API_KEY")
PLANETZERO_API_BASE = os.environ.get("PLANETZERO_API_BASE")
newclient = None


def initialize_client(engine):
    global newclient
    if newclient is None:
        if "gpt" in engine.lower():
            newclient = OpenAI(
                api_key=PLANETZERO_API_KEY,
                base_url=PLANETZERO_API_BASE,
            )


def construct_knowledge_graph_by_LLM(text, output_csv="knowledge_graph_LLM.csv"):
    """
    解析输入文本，通过大语言模型生成知识图谱并存储为 CSV 文件。
    :param text: 输入的文本内容。
    :param output_csv: 保存知识图谱的 CSV 文件路径。
    :return: 生成的 CSV 文件路径。
    """
    prompt = (
        "根据以下文本内容，提取有意义的知识图谱关系并按如下格式生成：\n"
        "\"Source\", \"Target\", \"Relation\"\n\n"
        f"文本内容：{text}\n\n"
        "注意：确保生成的关系有逻辑性，适用于知识图谱的构建。"
    )
    
    try:
        # 调用 GPT-4 或其他大语言模型生成知识图谱
        result = send_request_to_api(prompt, "生成知识图谱", temperature=0.2)
        lines = result.strip().split("\n")
        
        # 写入 CSV 文件
        with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Source", "Target", "Relation"])  # 写入表头
            for line in lines:
                if "," in line:
                    cleaned_line = [col.strip().strip('"') for col in line.split(",")]  # 去除多余引号和空格
                    writer.writerow(cleaned_line)
                    # writer.writerow([col.strip() for col in line.split(",")])
        
        return output_csv
    
    except Exception as e:
        print(f"Error while generating knowledge graph: {e}")
        return None


def send_request_to_api(knowledge_graph_content, user_query, temperature=0.1, engine="gpt-4-turbo"):
    """
    通过 API 向大模型发送请求，生成结果。
    :param knowledge_graph_content: 提示词内容，用于生成知识图谱。
    :param user_query: 用户查询内容。
    :param temperature: 控制输出多样性的参数。
    :param engine: 使用的大语言模型。
    :return: 模型生成的响应。
    """
    try:
        # 初始化 OpenAI 客户端（注意将 API 密钥配置为环境变量）
        client = ChatCompletion(api_key=os.getenv("OPENAI_API_KEY"))
        messages = [
            {"role": "system", "content": "You are an AI assistant for building structured knowledge graphs."},
            {"role": "user", "content": knowledge_graph_content},
            {"role": "user", "content": user_query}
        ]
        response = client.create(
            model=engine,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message["content"]
    
    except Exception as e:
        print(f"API Request failed: {e}")
        raise


# def send_request_to_api(knowledge_graph_content, user_query, temperature=0.1, engine="gpt-4-turbo"):
#     initialize_client(engine)

#     messages = [
#         {"role": "system", "content": "You are an AI assistant that helps people find information."},
#         {"role": "user", "content": knowledge_graph_content},
#         {"role": "user", "content": user_query}
#     ]

#     print(messages)

#     f = 0
#     while(f == 0):
#         try:
#             completion = newclient.chat.completions.create(
#                 model=engine,
#                 messages=messages,
#                 temperature=temperature,
#             )
#             result = completion.choices[0].message.content
#             f = 1
#         except Exception as e:
#             print(e)
#             print(engine + " error, retry")
#             time.sleep(2)
#     print(result)
#     return result

if __name__ == '__main__':
    knowledge_graph_content = '知识图谱内容示例'
    user_query = '用户提问示例'
    response = send_request_to_api(knowledge_graph_content, user_query)
    print(response)
