





from typing import List, Tuple
import networkx as nx
from difflib import SequenceMatcher  # 用于简单的字符串相似度计算

def semantic_match(node: str, query: str, threshold: float = 0.7) -> bool:
    """
    检查节点是否与查询语义匹配（基于字符串相似度）
    :param node: 图中的节点
    :param query: 用户输入的问题
    :param threshold: 相似度阈值，默认为0.7
    :return: 是否匹配
    """
    similarity = SequenceMatcher(None, node.lower(), query.lower()).ratio()
    return similarity >= threshold

# def retrieve_from_graph(graph: nx.Graph, query: str) -> List[Tuple[str, str, str]]:
#     """
#     在知识图谱中检索答案，返回匹配节点及其关联的三元组
#     :param graph: NetworkX图
#     :param query: 用户输入的问题
#     :return: 包含语义匹配节点及其关系的三元组列表
#     """
#     matched_nodes = []
#     results = []

#     # 1. 找到所有语义上匹配或相似的节点
#     for node in graph.nodes:
#         if semantic_match(node, query):
#             matched_nodes.append(node)

#     # 2. 遍历每个匹配节点的连通节点（限制总数小于20）
#     visited_nodes = set()
#     for matched_node in matched_nodes:
#         if len(visited_nodes) >= 20:  # 限制最大节点数
#             break

#         # 遍历与匹配节点直接相连的节点
#         neighbors = list(graph.neighbors(matched_node))
#         for neighbor in neighbors:
#             if neighbor not in visited_nodes:
#                 # 添加三元组到结果
#                 edge_data = graph.get_edge_data(matched_node, neighbor)
#                 edge_label = edge_data.get("relation", "connected")  # 边的关系属性，默认为"connected"
#                 results.append((matched_node, edge_label, neighbor))
#                 visited_nodes.add(neighbor)

#         # 确保匹配节点本身也被标记为访问过
#         visited_nodes.add(matched_node)

#     return results

from typing import List, Tuple

def retrieve_from_graph(graph: nx.Graph, query: str) -> List[Tuple[str, str, str]]:
    """
    在知识图谱中检索答案，返回匹配节点及其关联的三元组。
    :param graph: NetworkX 图
    :param query: 用户输入的问题
    :return: 包含语义匹配节点及其关系的三元组列表
    """
    matched_nodes = []
    results = []

    # 1. 找到所有语义上匹配或相似的节点
    for node in graph.nodes:
        if semantic_match(node, query):  # 使用自定义的语义匹配函数
            matched_nodes.append(node)

    # 2. 遍历每个匹配节点的连通节点（限制总数小于20）
    visited_nodes = set()
    for matched_node in matched_nodes:
        if len(visited_nodes) >= 20:  # 限制最大节点数
            break

        # 遍历与匹配节点直接相连的节点
        neighbors = list(graph.neighbors(matched_node))
        for neighbor in neighbors:
            if neighbor not in visited_nodes:
                # 添加三元组到结果
                edge_data = graph.get_edge_data(matched_node, neighbor)
                edge_label = edge_data.get("label", "connected")  # 边的关系属性，默认为"connected"
                results.append((matched_node, edge_label, neighbor))
                visited_nodes.add(neighbor)

        # 确保匹配节点本身也被标记为访问过
        visited_nodes.add(matched_node)

    return results
