from zhipuai import ZhipuAI


client = ZhipuAI(api_key="0ed124e225edb8eac72f60a320991d38.2he6rOqpIWdK2z72")

def ask_zhipu_with_kg(knowledge_graph_context, question):
    """
    使用知识图谱内容和用户问题调用智谱AI
    :param knowledge_graph_context: 知识图谱上下文（文本描述）
    :param question: 用户输入的问题
    :return: 智谱AI的回答
    """
    
    # 准备对话历史
    messages = [
        {"role": "system", "content": "你是一名知识图谱专家，能够结合知识图谱回答用户问题。"},
        {"role": "user", "content": f"以下是知识图谱内容：\n{knowledge_graph_context}"},
        {"role": "assistant", "content": "我已经获取了知识图谱内容，请告诉我您的问题。"},
        {"role": "user", "content": question}
    ]

    # 调用智谱AI
    response = client.chat.completions.create(
        model="glm-4",  # 替换为您的模型名称
        messages=messages,
    )
    print(response)

    answer = response.choices[0].message.content
    print("answer:_______________")
    print(answer)
    return answer

# 假设 response 是你提供的 Completion 对象


"""
Completion(
    model='glm-4-plus', 
    created=1733397111, 
    choices=[
        CompletionChoice(
            index=0, 
            finish_reason='stop', 
            message=CompletionMessage(
                content='“算法”是一个广泛的概念，涉及多个领域和应用。在计算机科学中，算法是指解决特定问题的明确、有序的步骤集合。简单来说，算法就是一系列指令，用来完成特定的任务。\n\n### 算法的基本特征\n1. **确定性**：算法的每个步骤都有明确的定义，不会产生歧义。\n2. **有限性**：算法必须在有限的步骤内完成。\n3. **输入**：算法可以有零个或多个输入。\n4. **输出**：算法至少产生一个输出。\n5. **有效性**：算法的每个步骤都必须是可行的。\n\n### 常见的算法类型\n1. **排序算法**：如冒泡排序、快速排序、归并排序等。\n2. **搜索算法**：如二分查找、深度优先搜索、广度优先搜索等。\n3. **图算法**：如Dijkstra算法、A*算法、最小生成树算法等。\n4. **动态规划**：用于解决多阶段决策问题。\n5. **贪心算法**：在每一步选择中都采取当前状态下最优的选择。\n\n### 应用领域\n- **数据分析**：用于数据清洗、特征选择等。\n- **人工智能**：如机器学习中的各种算法（决策树、神经网络等）。\n- **网络技术**：路由算法、加密算法等。\n- **图形图像处理**：图像识别、图像压缩等。\n\n### 如何设计和分析算法\n1. **理解问题**：明确问题的需求和限制。\n2. **设计算法**：选择合适的数据结构和算法类型。\n3. **实现算法**：用编程语言实现算法。\n4. **测试和调试**：验证算法的正确性和效率。\n5. **分析算法**：评估算法的时间复杂度和空间复杂度。\n\n如果您有更具体的问题或需要了解某个特定算法的细节，请提供更多信息，我会尽力提供详细的解答。', 
                role='assistant', 
                tool_calls=None
            )
        )
    ], 
    request_id='20241205191139ac5bfc3fed824218', 
    id='20241205191139ac5bfc3fed824218', 
    usage=CompletionUsage(prompt_tokens=47, completion_tokens=392, total_tokens=439)
)
"""

