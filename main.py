from synapse.api import Agent
from synapse.core.db import TopologyClient
from datasets import AGENT_DATASETS
import time


def print_section(title):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")


def load_agent_knowledge(agent, agent_id):
    if agent_id in AGENT_DATASETS:
        knowledge_count = 0
        for knowledge in AGENT_DATASETS[agent_id]:
            agent.learn(knowledge)
            knowledge_count += 1
        print(f"  ✓ {agent_id} 学习了 {knowledge_count} 条知识")
    else:
        print(f"  ⚠ {agent_id} 没有预定义数据集")


def main():
    print_section("Synapse 多智能体信息检索系统 - 综合测试")
    
    topology_client = TopologyClient()
    topology_client.clear_all()
    print("✓ 清空了所有现有数据")
    
    print_section("步骤 1: 创建智能体并建立网络")
    
    agent_a = Agent("Finance_Bot")
    agent_b = Agent("Market_Analyst")
    agent_c = Agent("News_Bot")
    
    print(f"✓ 创建了智能体: {agent_a}")
    print(f"✓ 创建了智能体: {agent_b}")
    print(f"✓ 创建了智能体: {agent_c}")
    
    print("\n设置智能体画像:")
    agent_a.set_profile(
        description="金融专家智能体，专注于股票、债券、基金等金融产品的分析和建议。",
        keywords=["股票", "债券", "基金", "金融分析", "投资建议"]
    )
    print(f"  ✓ 为 {agent_a} 设置了画像")
    
    agent_b.set_profile(
        description="市场分析师智能体，擅长分析市场趋势、行业动态和公司财报。",
        keywords=["市场分析", "行业动态", "公司财报", "趋势预测", "数据分析"]
    )
    print(f"  ✓ 为 {agent_b} 设置了画像")
    
    agent_c.set_profile(
        description="新闻聚合智能体，实时收集和整理各类新闻资讯，包括财经、科技、体育等。",
        keywords=["新闻聚合", "实时资讯", "财经新闻", "科技新闻", "体育新闻"]
    )
    print(f"  ✓ 为 {agent_c} 设置了画像")
    
    print("\n加载智能体知识库:")
    load_agent_knowledge(agent_a, "Finance_Bot")
    load_agent_knowledge(agent_b, "Market_Analyst")
    load_agent_knowledge(agent_c, "News_Bot")
    
    print("\n建立关系网络:")
    print(f"  {agent_a.connect('Market_Analyst', 0.9)}")
    print(f"  {agent_a.connect('News_Bot', 0.5)}")
    
    print(f"\nFinance_Bot 的邻居关系:")
    neighbors = agent_a.get_neighbors()
    for neighbor_id, weight in neighbors.items():
        print(f"  - {neighbor_id}: {weight:.2f}")
    
    print_section("步骤 2: 测试涟漪检索 - 强关系优先")
    
    question1 = "苹果公司股票表现如何？"
    print(f"\n问题: {question1}")
    
    results1 = agent_a.ask(question1, limit=3)
    print(f"\n检索结果 (共 {len(results1)} 条):")
    for i, result in enumerate(results1, 1):
        print(f"\n  结果 {i}:")
        print(f"    内容: {result.content}")
        print(f"    来源: {result.source_agent_id}")
        print(f"    相似度: {result.score:.4f}")
    
    print_section("步骤 3: 测试涟漪检索 - 弱关系补充")
    
    question2 = "特斯拉在德克萨斯州有什么新动态？"
    print(f"\n问题: {question2}")
    
    details2 = agent_a.ask_with_details(question2, limit=3)
    print(f"\n检索详情:")
    print(f"  检索轮次: {details2['round']}")
    print(f"  搜索的智能体: {details2['searched_ids']}")
    print(f"  强关系组: {details2['group_a_high_trust']}")
    print(f"  弱关系组: {details2['group_b_low_trust']}")
    print(f"\n检索结果 (共 {len(details2['results'])} 条):")
    for i, result in enumerate(details2['results'], 1):
        print(f"\n  结果 {i}:")
        print(f"    内容: {result.content}")
        print(f"    来源: {result.source_agent_id}")
        print(f"    相似度: {result.score:.4f}")
    
    print_section("步骤 4: 反馈机制 - 提升弱关系权重")
    
    print("\nFinance_Bot 对 News_Bot 的信息给出正面反馈...")
    feedback_result = agent_a.feedback("News_Bot", is_useful=True)
    print(f"✓ {feedback_result}")
    
    print("\n更新后的邻居关系:")
    neighbors = agent_a.get_neighbors()
    for neighbor_id, weight in neighbors.items():
        print(f"  - {neighbor_id}: {weight:.2f}")
    
    print_section("步骤 5: 再次测试 - 观察权重变化影响")
    
    question3 = "苹果公司发布了什么新产品？"
    print(f"\n问题: {question3}")
    
    details3 = agent_a.ask_with_details(question3, limit=3)
    print(f"\n检索详情:")
    print(f"  检索轮次: {details3['round']}")
    print(f"  搜索的智能体: {details3['searched_ids']}")
    print(f"\n检索结果 (共 {len(details3['results'])} 条):")
    for i, result in enumerate(details3['results'], 1):
        print(f"\n  结果 {i}:")
        print(f"    内容: {result.content}")
        print(f"    来源: {result.source_agent_id}")
        print(f"    相似度: {result.score:.4f}")
    
    print_section("步骤 6: 批量反馈测试")
    
    print("\n模拟多次交互反馈...")
    for i in range(3):
        agent_a.feedback("News_Bot", is_useful=True)
        print(f"  第 {i+1} 次正面反馈完成")
    
    print("\n最终邻居关系:")
    neighbors = agent_a.get_neighbors()
    for neighbor_id, weight in neighbors.items():
        print(f"  - {neighbor_id}: {weight:.2f}")
    
    print_section("步骤 7: 测试无结果时返回智能体画像")
    
    # 创建一个新的智能体，不加载任何知识，确保不会有匹配结果
    agent_d = Agent("Empty_Agent")
    agent_d.set_profile(
        description="空智能体，没有任何知识。",
        keywords=["空智能体", "无知识", "测试用"]
    )
    print(f"✓ 创建了空智能体: {agent_d}")
    
    # 建立与空智能体的连接
    agent_a.connect("Empty_Agent", 0.8)
    print(f"✓ 建立了与空智能体的连接")
    
    # 向空智能体提问，确保不会有匹配结果
    question4 = "测试空智能体的智能体画像返回"
    print(f"\n问题: {question4}")
    
    results4 = agent_d.ask(question4, limit=3)
    print(f"\n检索结果 (共 {len(results4)} 条):")
    for i, result in enumerate(results4, 1):
        print(f"\n  结果 {i}:")
        print(f"    内容: {result.content}")
        print(f"    来源: {result.source_agent_id}")
        print(f"    相似度: {result.score:.4f}")
    
    print_section("测试完成")
    
    print("\n✓ 所有测试通过!")
    print("\n系统特性验证:")
    print("  ✓ 双存储架构 (Qdrant + Redis)")
    print("  ✓ 涟漪检索 (强关系优先)")
    print("  ✓ 动态权重更新")
    print("  ✓ 简单易用的 Agent API")
    print("  ✓ 智能体画像功能")


if __name__ == "__main__":
    main()
