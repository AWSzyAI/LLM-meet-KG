import streamlit as st
from graph_construction import construct_knowledge_graph, graph_to_dict
from question_answering import retrieve_from_graph
from zhipu_api import ask_zhipu_with_kg
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib import rcParams
from matplotlib import font_manager as fm
from gpt_api import send_request_to_api
import numpy as np

# 缓存知识图谱内容
uploaded_graph = {"graph": None, "graph_dict": None}
font_path = "./simfang.ttf"
def draw_graph(graph, font_path="simfang.ttf"):
    """绘制知识图谱为动态图"""
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=2000, font_size=10, font_weight="bold", edge_color="gray")
    labels = nx.get_edge_attributes(graph, "relation")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    
    # 设置中文字体
    try:
        font_prop = fm.FontProperties(fname=font_path)
        rcParams["font.family"] = font_prop.get_name()
    except Exception as e:
        print(f"字体加载失败，请检查字体路径: {e}")
    
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()  # 确保关闭图像，释放内存
    return buf

def render_chat_history(chat_history):
    """渲染对话历史为类似 ChatGPT 的界面"""
    for entry in chat_history:
        # 用户消息
        st.markdown(
            f"""
            <div style="background-color:#f0f0f0; padding:10px; border-radius:10px; margin-bottom:5px;">
                <strong>用户:</strong> {entry['user']}
            </div>
            """, unsafe_allow_html=True)
        # 系统消息
        st.markdown(
            f"""
            <div style="background-color:#dff0d8; padding:10px; border-radius:10px; margin-bottom:10px;">
                <strong>系统:</strong> {entry['assistant']}
            </div>
            """, unsafe_allow_html=True)

def main():
    st.title("知识图谱增强LLM")
    
    with st.chat_message("user"):
        st.write("Hello 👋")
    with st.chat_message("assistant"):
        st.write("Hello human")
        st.bar_chart(np.random.randn(30, 3))
        
    # 上传文件
    uploaded_file = st.file_uploader("上传文件", type=["csv"])
    
    if uploaded_file is not None:
        # 构建知识图谱并缓存
        if uploaded_graph["graph"] is None:
            # 读取已有知识图谱

            # 增量构建
            graph = construct_knowledge_graph(uploaded_file)
            graph_dict = graph_to_dict(graph)
            uploaded_graph["graph"] = graph
            uploaded_graph["graph_dict"] = graph_dict
            st.success("知识图谱已成功构建！")
            
            # 保存新的知识图谱到文件

            # 可视化
            st.json(graph_dict)  # 可视化知识图谱结构
            
            # 可视化知识图谱
            graph_img = draw_graph(graph)
            st.image(graph_img, caption="知识图谱结构", use_column_width=True)

    # 多轮对话部分
    if uploaded_graph["graph"] is not None:
        st.subheader("多轮对话")
        
        # 初始化会话历史
        if "dialog_history" not in st.session_state:
            st.session_state["dialog_history"] = []
        
        # 显示历史对话
        render_chat_history(st.session_state["dialog_history"])
        
        # 用户输入
        user_input = st.text_input("请输入问题", key="user_input")
        # if user_input:
            # 知识图谱检索
        graph = uploaded_graph["graph"]
        matches = retrieve_from_graph(graph, user_input)
        context = ", ".join(matches) if matches else "未检索到相关信息"
    

        # 调用智谱API
        # answer = ask_zhipu_with_kg(context, user_input)
        answer = send_request_to_api(context,user_input,engine="gpt-4-turbo")
        
        
        # 更新历史对话
        st.session_state["dialog_history"].append({"user": user_input, "assistant": answer})


if __name__ == "__main__":
    main()
