# Synapse 多智能体信息检索系统

## 项目概述
Synapse是一个创新的多智能体信息检索系统，通过构建智能体网络和采用涟漪搜索算法，实现了高效、智能的信息检索。该系统将传统的单一检索模式升级为多智能体协作模式，模拟人类社交网络的信息传播方式，提高了信息检索的相关性和可靠性。

## 核心功能

### 1. 多智能体网络构建
- 支持创建多个专业领域智能体（如Finance_Bot、Market_Analyst、News_Bot等）
- 智能体间可建立信任关系，权重范围0-1
- 支持动态调整智能体间的信任权重

### 2. 涟漪搜索算法
- **分级搜索机制**：
  - 第一轮：优先搜索高信任度邻居（信任权重 ≥ 高信任阈值）
  - 第二轮：若结果置信度不足，扩展至低信任度邻居
- **智能结果过滤**：基于相似度得分筛选最相关结果
- **详细搜索过程**：提供完整搜索轮次和涉及智能体信息

### 3. 动态学习与反馈
- 智能体可通过`learn()`方法学习新知识
- 支持基于交互结果的反馈机制
- 自动调整智能体间的信任权重

### 4. 双存储架构
- **向量数据库**：存储智能体知识，支持相似性检索
  - 支持多种后端：Qdrant、Milvus、Weaviate、ChromaDB、pgvector
- **拓扑数据库**：存储智能体关系网络
  - 支持多种后端：Redis、Neo4j、ArangoDB

## 与传统检索模型的区别

| 传统检索 | Synapse多智能体检索 |
|---------|-------------------|
| 单一检索源，信息孤岛 | 多智能体协作，信息网络 |
| 固定检索范围，无优先级 | 基于信任度，分级搜索 |
| 静态检索，无学习能力 | 动态学习，持续进化 |
| 无反馈机制，结果固定 | 基于反馈调整，结果优化 |

## 系统架构

### 1. 智能体模型
- **Agent类**：表示单个智能体，包含id、名称、专业领域、知识向量等属性
- **Relationship类**：表示智能体间的信任关系，包含源智能体、目标智能体、信任权重等属性

### 2. 检索流程
1. **初始检索**：用户通过主智能体发起检索请求
2. **涟漪扩散**：主智能体向其信任的邻居智能体扩散请求
3. **结果收集**：收集各智能体的检索结果
4. **结果过滤**：基于相似度得分筛选最相关结果
5. **结果返回**：将最终结果返回给用户
6. **反馈学习**：根据用户反馈调整智能体间的信任权重

### 3. 数据库模型
- **向量数据库**：
  - 表结构：agent_id, knowledge_vector, metadata
  - 支持向量相似度查询
- **拓扑数据库**：
  - 表结构：source_agent_id, target_agent_id, trust_weight, last_updated
  - 支持图查询，快速找到智能体的邻居

## 快速开始

### 1. 环境搭建
- Python 3.8+
- 安装依赖：`pip install -r requirements.txt`

### 2. 启动数据库
- 使用Docker启动测试数据库：`bash start_test_databases.sh`
- 或手动配置向量数据库和拓扑数据库

### 3. 运行示例
```python
from synapse.api import Agent, Synapse

# 创建Synapse实例
synapse = Synapse()

# 创建智能体
agent1 = Agent(id="Finance_Bot", name="金融智能体", domain="金融")
agent2 = Agent(id="Market_Analyst", name="市场分析师", domain="市场分析")
agent3 = Agent(id="News_Bot", name="新闻智能体", domain="新闻")

# 添加智能体到系统
synapse.add_agent(agent1)
synapse.add_agent(agent2)
synapse.add_agent(agent3)

# 建立智能体间的信任关系
synapse.add_relationship("Finance_Bot", "Market_Analyst", 0.8)
synapse.add_relationship("Market_Analyst", "News_Bot", 0.7)

# 智能体学习知识
agent1.learn(["2024年全球经济增长预计为3.1%"])
agent2.learn(["科技股在过去一年上涨了25%"])
agent3.learn(["美联储决定维持利率不变"])

# 执行检索
results = synapse.retrieve("Finance_Bot", "2024年经济趋势")
print(results)
```

### 4. API参考

#### Agent类
```python
class Agent:
    def __init__(self, id, name, domain):
        # 初始化智能体
        pass
    
    def learn(self, knowledge_items):
        # 学习新知识
        pass
    
    def retrieve(self, query):
        # 检索知识
        pass
```

#### Synapse类
```python
class Synapse:
    def __init__(self):
        # 初始化系统
        pass
    
    def add_agent(self, agent):
        # 添加智能体
        pass
    
    def add_relationship(self, source_agent_id, target_agent_id, trust_weight):
        # 添加智能体关系
        pass
    
    def retrieve(self, main_agent_id, query, high_trust_threshold=0.7, low_trust_threshold=0.3, max_rounds=2, max_results=5):
        # 执行涟漪检索
        pass
```

## 应用场景

1. **专业领域知识检索**：金融、医疗、法律等专业领域的深度知识检索
2. **分布式信息系统**：企业内部多部门信息共享与检索
3. **智能助手网络**：构建智能助手协作网络，提供更全面的服务
4. **知识图谱扩展**：动态扩展和优化知识图谱
5. **决策支持系统**：为复杂决策提供多源信息支持

## 项目结构

```
syn/
├── main.py              # 主程序，演示系统功能
├── synapse/
│   ├── api.py           # Agent API定义
│   ├── core/
│   │   ├── db/          # 数据库客户端
│   │   │   ├── vector_client.py      # 向量数据库客户端
│   │   │   └── topology_client.py    # 拓扑数据库客户端
│   │   ├── retriever/   # 检索引擎
│   │   │   └── ripple_search.py      # 涟漪搜索实现
│   │   └── feedback/    # 反馈机制
│   └── utils/           # 工具函数
├── datasets.py          # 智能体知识库
├── test_databases.py    # 数据库测试脚本
├── docker-compose-all-dbs.yml  # 所有数据库的Docker配置
├── start_test_databases.sh     # 启动测试数据库脚本
└── requirements.txt     # 项目依赖
```

## 测试框架
系统提供了完整的数据库测试框架：
- 支持8种不同数据库的性能测试
- 测试指标包括：向量查询时间、关系查询时间、存储效率等
- 提供详细的测试报告和对比分析

## 未来展望

1. **智能体自动生成**：根据需求自动生成专业领域智能体
2. **更复杂的信任模型**：引入多维度信任评估
3. **实时数据更新**：支持从外部数据源实时更新知识
4. **可视化界面**：提供智能体网络和搜索过程的可视化
5. **多语言支持**：扩展到多语言环境

## 总结
Synapse多智能体信息检索系统通过创新的涟漪搜索算法和动态信任关系网络，实现了比传统检索模式更高效、更智能的信息检索。该系统具有良好的扩展性和适应性，可广泛应用于各种专业领域和复杂信息检索场景。

## 贡献者

<div align="center">
  <a href="https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=BOMBFUOCK/Multi-Agent-RAG-Synapse" alt="Contributors" />
  </a>
</div>

---

项目地址：https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse.git
联系人：ykd1374991239@163.com
