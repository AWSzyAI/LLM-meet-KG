import PyPDF2
import pandas as pd
from tqdm import tqdm
import spacy
from gpt_api import construct_knowledge_graph_by_LLM, send_request_to_api

if __name__ == "__main__":
    # 打开 PDF 文件
    pdf_file = open('2024-12-06.pdf', 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # 提取 PDF 中的文本
    text = ''
    for page in tqdm(pdf_reader.pages, desc="提取PDF中的文本"):
        text += page.extract_text()

    # 使用 GPT 进一步优化和生成更准确的知识图谱
    output_csv = "pdf_knowledge_graph.csv"
    output_path = construct_knowledge_graph_by_LLM(text, output_csv=output_csv)

    if output_path:
        print(f"知识图谱已生成并保存在：{output_path}")
    else:
        print("知识图谱生成失败！")
