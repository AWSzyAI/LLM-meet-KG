import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib import font_manager as fm
from pyvis.network import Network

from api.gpt_api import send_request_to_api
from api.zhipu_api import ask_zhipu_with_kg

from graph_construction import construct_knowledge_graph, graph_to_dict
from question_answering import retrieve_from_graph


uploaded_graph = {"graph": None, "graph_dict": None}

def draw_interactive_graph(graph):
    """
    使用 PyVis 绘制交互式知识图谱
    return pyvis.network.Network
    """
    # net = Network(height="500px", width="100%", notebook=True)
    net = Network(height="500px", width="100%", notebook=True, cdn_resources='remote')
    
    for node in graph.nodes:
        net.add_node(node, label=str(node))
    for edge in graph.edges(data=True):
        source, target, attr = edge
        label = attr.get("label", "")
        net.add_edge(source, target, title=label, label=label)
    return net

def render_chat_history(chat_history):
    """渲染对话历史"""
    for entry in chat_history:
        st.markdown(
            f"""
            <div style="background-color:#111111; padding:10px; border-radius:10px;">
                <strong>用户:</strong> {entry['user']}
            </div>
            <div style="background-color:#000000; padding:10px; border-radius:10px; margin-top:5px;">
                <strong>系统:</strong> {entry['assistant']}
            </div>
            """, unsafe_allow_html=True
        )

def main():
    st.title("LLM meet KG")
    uploaded_file = st.file_uploader("上传文件（CSV 格式,可通过pdf2csv.py生成）", type=["csv"])
    
    if uploaded_file:
        if uploaded_graph["graph"] is None:
            try:
                graph = construct_knowledge_graph(uploaded_file)
                graph_dict = graph_to_dict(graph)
                uploaded_graph["graph"] = graph
                uploaded_graph["graph_dict"] = graph_dict
                st.success("知识图谱已成功构建！")

                # 可视化知识图谱
                st.json(graph_dict, expanded=False)
                interactive_graph = draw_interactive_graph(graph)
                try:
                    interactive_graph.show("static/graph.html")
                    st.components.v1.html(open("static/graph.html", "r").read(), height=500)
                except Exception as e:
                    st.error(f"图形显示失败: {e}")
            except Exception as e:
                st.error(f"知识图谱构建失败：{e}")

    if uploaded_graph["graph"] is not None:
        st.subheader("智能对话")

        # 初始化对话历史
        if "dialog_history" not in st.session_state:
            st.session_state["dialog_history"] = []

        render_chat_history(st.session_state["dialog_history"])

        # 用户输入框
        user_input = st.text_input("请输入问题", key="user_input")

        if st.button("提交") and user_input:
            graph = uploaded_graph["graph"]
            
            # 从图谱中检索相关信息
            matches = retrieve_from_graph(graph, user_input)
            if matches:
                matches_graph = nx.DiGraph()
                for match in matches:  # matches 是一个列表
                    source, relation, target = match  # 解包三元组
                    matches_graph.add_edge(source, target, label=relation)
                interactive_matches_graph = draw_interactive_graph(matches_graph)
                interactive_matches_graph.show("static/graph.html")
                st.components.v1.html(open("static/graph.html", "r").read(), height=500)
            context = matches if matches else "未找到相关信息"
            print(f"matches: {matches}")  # Debugging output
            

            # 调用 API 获取系统回答
            # answer = send_request_to_api(context, user_input, engine="gpt-4-turbo")
            answer = ask_zhipu_with_kg(context, user_input)
            print(f"Answer: {answer}")  # Debugging output

            # 更新会话历史
            st.session_state["dialog_history"].append({"user": user_input, "assistant": answer})

            # 刷新对话历史
            render_chat_history(st.session_state["dialog_history"])
            

            # st.session_state.user_input = ""
            # st.experimental_set_query_params(reload="true") # 旧版 API
            st.query_params.update({"reload": "true"})
if __name__ == "__main__":
    main()