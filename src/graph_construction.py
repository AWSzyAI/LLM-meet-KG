import networkx as nx
import pandas as pd

def construct_knowledge_graph(file_path):
    """
    从上传的文件中构建知识图谱
    type: 
    """
    df = pd.read_csv(file_path)
    # 清理列名
    df.columns = df.columns.str.strip()  # 去掉首尾空格
    required_columns = {'Source', 'Target', 'Relation'}
    
    # 检查文件是否包含所需的列
    if not required_columns.issubset(df.columns):
        raise ValueError(f"文件中缺少必要列: {required_columns - set(df.columns)}")
    
    graph = nx.DiGraph()
    for _, row in df.iterrows():
        source = row['Source']
        target = row['Target']
        relation = row['Relation']
        graph.add_edge(source, target, label=relation)
    
    return graph

def graph_to_dict(graph):
    """
    将NetworkX图转为字典，供前端可视化
    """
    nodes = [{"id": node, "label": node} for node in graph.nodes]
    edges = [
        {"source": u, "target": v, "label": data['label']}
        for u, v, data in graph.edges(data=True)
    ]
    return {"nodes": nodes, "edges": edges}



# import networkx as nx
# import pandas as pd

# def construct_knowledge_graph(file_path):
#     """
#     从上传的文件中构建知识图谱
#     """
#     df = pd.read_csv(file_path)
#     # 清理列名
#     df.columns = df.columns.str.strip()  # 去掉首尾空格
#     required_columns = {'Source', 'Target', 'Relation'}
    
#     # 检查文件是否包含所需的列
#     if not required_columns.issubset(df.columns):
#         raise ValueError(f"文件中缺少必要列: {required_columns - set(df.columns)}")
    
#     graph = nx.DiGraph()
#     for _, row in df.iterrows():
#         source = row['Source']
#         target = row['Target']
#         relation = row['Relation']
#         graph.add_edge(source, target, label=relation)
    
#     return graph

# def graph_to_dict(graph):
#     """
#     将NetworkX图转为字典，供前端可视化
#     """
#     nodes = [{"id": node, "label": node} for node in graph.nodes]
#     edges = [
#         {"source": u, "target": v, "label": data['label']}
#         for u, v, data in graph.edges(data=True)
#     ]
#     return {"nodes": nodes, "edges": edges}