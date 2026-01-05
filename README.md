<div align="center">
  <a href="#中文" style="padding: 8px 16px; margin: 0 8px; background-color: #2563eb; color: white; border-radius: 4px; text-decoration: none;">中文</a>
  <a href="#English" style="padding: 8px 16px; margin: 0 8px; background-color: #f3f4f6; color: #374151; border: 1px solid #e5e7eb; border-radius: 4px; text-decoration: none;">English</a>
</div>


<hr>

<h2 id="English">Synapse Multi-Agent Information Retrieval System</h2>

<div id="English-content">

# Synapse Multi-Agent Information Retrieval System

## Project Overview
Synapse is an innovative multi-agent information retrieval system that achieves efficient and intelligent information retrieval by building agent networks and adopting a ripple search algorithm. This system upgrades the traditional single retrieval mode to a multi-agent collaborative mode, simulating the information dissemination method of human social networks, and improving the relevance and reliability of information retrieval.

## Core Features

### 1. Multi-Agent Network Construction
- Support for creating multiple domain-specific agents (e.g., Finance_Bot, Market_Analyst, News_Bot, etc.)
- Agents can establish trust relationships with weight range 0-1
- Support for dynamic adjustment of trust weights between agents

### 2. Ripple Search Algorithm
- **Hierarchical Search Mechanism**:
  - First round: Prioritize searching high-trust neighbors (trust weight ≥ high trust threshold)
  - Second round: If result confidence is insufficient, expand to low-trust neighbors
- **Intelligent Result Filtering**: Filter most relevant results based on similarity scores
- **Detailed Search Process**: Provide complete search rounds and involved agent information

### 3. Dynamic Learning and Feedback
- Agents can learn new knowledge through the `learn()` method
- Support for feedback mechanisms based on interaction results
- Automatically adjust trust weights between agents

### 4. Dual Storage Architecture
- **Vector Database**: Stores agent knowledge, supports similarity retrieval
  - Supports multiple backends: Qdrant, Milvus, Weaviate, ChromaDB, pgvector
- **Topology Database**: Stores agent relationship networks
  - Supports multiple backends: Redis, Neo4j, ArangoDB

## Differences from Traditional Retrieval Models

| Traditional Retrieval | Synapse Multi-Agent Retrieval |
|----------------------|-------------------------------|
| Single retrieval source, information silos | Multi-agent collaboration, information network |
| Fixed retrieval scope, no priority | Trust-based, hierarchical search |
| Static retrieval, no learning ability | Dynamic learning, continuous evolution |
| No feedback mechanism, fixed results | Feedback-based adjustment, result optimization |
| Single vector database dependency | Supports multiple database backends, flexible expansion |

## Technical Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    Synapse System Architecture               │
├─────────┬─────────┬───────────────────────────────────────────┤
│  Agent  │         │  Core Components                         │
│  API    │         ├─────────────────────┬─────────────────────┤
│         │         │  Retrieval Engine   │  Data Storage       │
└─────────┴─────────┼─────────────────────┼─────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│                 Ripple Searcher                              │
└───────────────────────────────────────────────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│  VectorDBClient                 │  TopologyClient            │
└───────────────────────────────────────────────────────────────┘
                    │                      │
                    ▼                      ▼
┌─────────────────────────┐    ┌───────────────────────────┐
│  Vector Database        │    │  Topology/Graph Database  │
│  (Qdrant/Milvus/...)    │    │  (Redis/Neo4j/...)        │
└─────────────────────────┘    └───────────────────────────┘
```

## Core Component Description

### Agent Class
- **Core API**: Provides a unified agent interaction interface
- **Main Methods**:
  - `learn(text, metadata)`: Learn new knowledge
  - `ask(question, limit)`: Execute ripple search
  - `ask_with_details(question, limit)`: Search with detailed process
  - `feedback(target_agent_id, is_useful)`: Feedback mechanism
  - `connect(target_agent_id, weight)`: Establish agent connection

### RippleSearcher
- **Search Strategy**: Trust-based hierarchical search
- **Search Process**:
  1. Convert query to vector
  2. Get source agent's neighbor list
  3. Divide into high-trust group (Group A) and low-trust group (Group B) based on trust weights
  4. First round search: Query Group A and own vector database
  5. If result confidence is high, return directly; otherwise execute second round search
  6. Second round search: Query Group B's vector database
  7. Merge results and return sorted

### Dynamic Weight Management
- **Feedback-based Adjustment**: Positive feedback increases trust weight, negative feedback decreases
- **Adaptive Learning**: System continuously optimizes agent relationship network based on interaction history
- **Weight Range**: 0-1, 0 means no trust, 1 means complete trust

## Dataset Description
The system provides domain-specific knowledge bases for each agent, including:
- Finance_Bot: Financial domain knowledge (15 items)
- Market_Analyst: Market analysis knowledge (15 items)
- News_Bot: News domain knowledge (15 items)
- Tech_Expert: Technical expert knowledge (15 items)
- Economic_Analyst: Economic analysis knowledge (15 items)

## Database Support

### Vector Databases
1. Qdrant
2. Milvus
3. Weaviate
4. ChromaDB
5. pgvector

### Topology/Graph Databases
1. Redis
2. Neo4j
3. ArangoDB

## Quick Start

### Start Dependent Services
```bash
# Start all test databases (using Docker Compose)
./start_test_databases.sh
```

### Run Example
```bash
# Install dependencies
pip install -r requirements.txt

# Run main program
python main.py
```

### Basic Usage
```python
from synapse.api import Agent

# Create agents
agent_a = Agent("Finance_Bot")
agent_b = Agent("Market_Analyst")

# Establish connection
agent_a.connect("Market_Analyst", 0.9)

# Learn knowledge
agent_a.learn("Apple's Q1 2024 revenue increased by 10%")

# Execute search
results = agent_a.ask("How is Apple's stock performing?", limit=3)

# Feedback mechanism
agent_a.feedback("Market_Analyst", is_useful=True)
```

## System Call Flow

### 1. System Initialization Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. System Startup                                         │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Load Configuration File (config.yaml)                  │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Initialize Database Clients                            │
│  - Vector Database Client (VectorDBClient)                 │
│  - Topology Database Client (TopologyClient)               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Initialize Retrieval Engine (RippleSearcher)           │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. Initialize Weight Manager (WeightManager)              │
└────────────────────────────────────────────────────────────┘
```

### 2. Agent Creation and Network Construction Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Create Agent Instance                                  │
│  agent = Agent("Agent_ID")                                 │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Load Predefined Knowledge Base (Optional)              │
│  - Load domain-specific knowledge from datasets.py         │
│  - Call agent.learn() method to learn knowledge            │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Establish Agent Relationship Network                   │
│  - Call agent.connect(target_id, weight)                   │
│  - Relationships stored in topology database               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Verify Relationship Network                            │
│  - Call agent.get_neighbors() to check relationships       │
└────────────────────────────────────────────────────────────┘
```

### 3. Ripple Search Algorithm Execution Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Receive Query Request                                  │
│  results = agent.ask(question, limit)                      │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Query Text Vectorization                               │
│  - Generate vector using SentenceTransformers              │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Get Agent Neighbor List                                │
│  - Read relationship weights from topology database        │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Neighbor Grouping (Based on Trust Threshold)           │
│  - High Trust Group (Group A): Weight ≥ high_trust_threshold │
│  - Low Trust Group (Group B): Weight ≥ low_trust_threshold and < high_trust_threshold │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. First Round Search: High Trust Group + Self            │
│  - Query Group A agents and own vector database            │
│  - Collect results with highest similarity scores          │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. Result Confidence Evaluation                           │
│  - Check if highest score ≥ high_confidence_threshold      │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────┴────────────────┐     ┌─────────────────────────┐
│  Yes: Return Results       │     │  No: Second Round Search │
│  - Sort and return top-N results │  - Query Group B agents' vector databases │
└────────────────────────────┘     └───────────┬─────────────┘
                                               │
┌───────────────────────────────────────────────▼─────────────┐
│  7. Merge and Sort Results                                 │
│  - Merge results from both rounds                          │
│  - Sort by similarity score in descending order            │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  8. Return Final Results                                   │
│  - Return SearchResult list                                │
└────────────────────────────────────────────────────────────┘
```

### 4. Feedback Mechanism Execution Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Receive Feedback Request                               │
│  agent.feedback(target_id, is_useful=True)                │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Determine Feedback Type                                │
│  - positive: is_useful=True                                │
│  - negative: is_useful=False                               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Get Current Relationship Weight                        │
│  - Read current weight value from topology database        │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Calculate New Weight Value                             │
│  - Adjust weight based on feedback type                    │
│  - Ensure weight is within [0, 1] range                    │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. Update Topology Database                               │
│  - Write new weight to topology database                   │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. Return Update Result                                   │
│  - Return new weight value                                 │
└────────────────────────────────────────────────────────────┘
```

### 5. Complete System Call Example Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Start Services                                         │
│  ./start_test_databases.sh                                 │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Import Dependencies                                    │
│  from synapse.api import Agent                             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Create Agents                                          │
│  finance_agent = Agent("Finance_Bot")                      │
│  market_agent = Agent("Market_Analyst")                    │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Establish Agent Connections                            │
│  finance_agent.connect("Market_Analyst", 0.9)             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. Learn Knowledge                                        │
│  finance_agent.learn("Apple's Q1 2024 revenue increased by 10%") │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. Execute Retrieval                                      │
│  results = finance_agent.ask("How is Apple's stock performing?", limit=3) │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  7. Process Retrieval Results                              │
│  - Iterate through result list                             │
│  - Extract content, source, similarity score               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  8. Provide Feedback                                       │
│  finance_agent.feedback("Market_Analyst", is_useful=True) │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  9. Verify Weight Update                                   │
│  neighbors = finance_agent.get_neighbors()                 │
└────────────────────────────────────────────────────────────┘
```

## Project Features

1. **Innovation**: Breaks through traditional retrieval models, adopts multi-agent collaboration and ripple search
2. **Flexibility**: Supports multiple database backends, can be flexibly switched according to needs
3. **Scalability**: Easy to add new agents and expand new functional modules
4. **Adaptability**: Continuously optimized through feedback mechanisms, evolving over time
5. **Professionalism**: Designs agents for different fields, provides professional knowledge retrieval

## Application Scenarios

1. **Professional Domain Knowledge Retrieval**: Deep knowledge retrieval in professional fields such as finance, medical care, law, etc.
2. **Distributed Information Systems**: Enterprise internal multi-department information sharing and retrieval
3. **Intelligent Assistant Network**: Build intelligent assistant collaboration networks, provide more comprehensive services
4. **Knowledge Graph Expansion**: Dynamically expand and optimize knowledge graphs
5. **Decision Support Systems**: Provide multi-source information support for complex decisions

## Project Structure

```
syn/
├── main.py              # Main program, demonstrates system functionality
├── synapse/
│   ├── api.py           # Agent API definition
│   ├── core/
│   │   ├── db/          # Database clients
│   │   │   ├── vector_client.py      # Vector database client
│   │   │   └── topology_client.py    # Topology database client
│   │   ├── retriever/   # Retrieval engine
│   │   │   └── ripple_search.py      # Ripple search implementation
│   │   └── feedback/    # Feedback mechanism
│   └── utils/           # Utility functions
├── datasets.py          # Agent knowledge base
├── test_databases.py    # Database test scripts
├── docker-compose-all-dbs.yml  # Docker configuration for all databases
├── start_test_databases.sh     # Script to start test databases
└────────────────────────────────────────────────────────────┘
```

## Testing Framework
The system provides a complete database testing framework:
- Supports performance testing for 8 different databases
- Test metrics include: vector query time, relationship query time, storage efficiency, etc.
- Provides detailed test reports and comparative analysis

## Future Outlook

1. **Agent Auto-generation**: Automatically generate domain-specific agents based on requirements
2. **More Complex Trust Models**: Introduce multi-dimensional trust evaluation
3. **Real-time Data Updates**: Support real-time knowledge updates from external data sources
4. **Visualization Interface**: Provide visualization of agent networks and search processes
5. **Multi-language Support**: Expand to multi-language environments

## Summary
The Synapse Multi-Agent Information Retrieval System achieves more efficient and intelligent information retrieval than traditional retrieval models through innovative ripple search algorithms and dynamic trust relationship networks. This system has good scalability and adaptability, and can be widely applied to various professional fields and complex information retrieval scenarios.

---

Project Address: https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse.git
Contact: ykd1374991239@163.com
</div>

<hr>

<h2 id="中文">Synapse 多智能体信息检索系统</h2>

<div id="中文-content">

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
- **详细搜索过程**：提供完整的搜索轮次和涉及智能体信息

### 3. 动态学习与反馈
- 智能体可通过`learn()`方法学习新知识
- 支持基于交互结果的反馈机制
- 自动调整智能体间的信任权重

### 4. 双存储架构
- **向量数据库**：存储智能体知识，支持相似度检索
  - 支持多种后端：Qdrant、Milvus、Weaviate、ChromaDB、pgvector
- **拓扑数据库**：存储智能体关系网络
  - 支持多种后端：Redis、Neo4j、ArangoDB

## 与传统检索模式的区别

| 传统检索模式 | Synapse 多智能体检索 |
|-------------|----------------------|
| 单一检索源，信息孤岛 | 多智能体协作，信息网络 |
| 固定检索范围，无优先级 | 基于信任关系，分级搜索 |
| 静态检索，无学习能力 | 动态学习，持续进化 |
| 无反馈机制，结果固定 | 基于反馈调整，结果优化 |
| 单一向量数据库依赖 | 支持多种数据库后端，灵活扩展 |

## 技术架构

```
┌───────────────────────────────────────────────────────────────┐
│                      Synapse 系统架构                         │
├─────────┬─────────┬───────────────────────────────────────────┤
│  Agent  │         │  核心组件                                  │
│  API    │         ├─────────────────────┬─────────────────────┤
│         │         │  检索引擎           │  数据存储            │
└─────────┴─────────┼─────────────────────┼─────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│                  Ripple Searcher（涟漪搜索器）                │
└───────────────────────────────────────────────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│  VectorDBClient（向量数据库客户端）  │  TopologyClient（拓扑客户端） │
└───────────────────────────────────────────────────────────────┘
                    │                      │
                    ▼                      ▼
┌─────────────────────────┐    ┌───────────────────────────┐
│  向量数据库             │    │  拓扑/图数据库           │
│  (Qdrant/Milvus/...)    │    │  (Redis/Neo4j/...)        │
└─────────────────────────┘    └───────────────────────────┘
```

## 核心组件说明

### Agent 类
- **核心API**：提供统一的智能体交互接口
- **主要方法**：
  - `learn(text, metadata)`：学习新知识
  - `ask(question, limit)`：执行涟漪搜索
  - `ask_with_details(question, limit)`：带详细过程的搜索
  - `feedback(target_agent_id, is_useful)`：反馈机制
  - `connect(target_agent_id, weight)`：建立智能体连接

### RippleSearcher（涟漪搜索器）
- **搜索策略**：基于信任度的分级搜索
- **搜索流程**：
  1. 将查询转换为向量
  2. 获取源智能体的邻居列表
  3. 按信任权重分为高信任组（A组）和低信任组（B组）
  4. 第一轮搜索：查询A组和自身的向量数据库
  5. 若结果置信度高，直接返回；否则执行第二轮搜索
  6. 第二轮搜索：查询B组的向量数据库
  7. 合并结果并排序返回

### 动态权重管理
- **基于反馈的调整**：正面反馈增加信任权重，负面反馈减少
- **自适应学习**：系统根据交互历史不断优化智能体关系网络
- **权重范围**：0-1，0表示无信任，1表示完全信任

## 数据集说明
系统为每个智能体提供了专业领域知识库，包括：
- Finance_Bot：金融领域知识（15条）
- Market_Analyst：市场分析知识（15条）
- News_Bot：新闻领域知识（15条）
- Tech_Expert：技术专家知识（15条）
- Economic_Analyst：经济分析知识（15条）

## 数据库支持

### 向量数据库
1. Qdrant
2. Milvus
3. Weaviate
4. ChromaDB
5. pgvector

### 拓扑/图数据库
1. Redis
2. Neo4j
3. ArangoDB

## 快速开始

### 启动依赖服务
```bash
# 启动所有测试数据库（使用Docker Compose）
./start_test_databases.sh
```

### 运行示例
```bash
# 安装依赖
pip install -r requirements.txt

# 运行主程序
python main.py
```

### 基本使用
```python
from synapse.api import Agent

# 创建智能体
agent_a = Agent("Finance_Bot")
agent_b = Agent("Market_Analyst")

# 建立连接
agent_a.connect("Market_Analyst", 0.9)

# 学习知识
agent_a.learn("苹果公司2024年Q1营收增长10%")

# 执行搜索
results = agent_a.ask("苹果公司股票表现如何？", limit=3)

# 反馈机制
agent_a.feedback("Market_Analyst", is_useful=True)
```

## 系统调用流程

### 1. 系统初始化流程

```
┌────────────────────────────────────────────────────────────┐
│  1. 系统启动                                               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. 加载配置文件 (config.yaml)                             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. 初始化数据库客户端                                     │
│  - 向量数据库客户端 (VectorDBClient)                      │
│  - 拓扑数据库客户端 (TopologyClient)                      │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. 初始化检索引擎 (RippleSearcher)                       │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. 初始化权重管理器 (WeightManager)                      │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. 系统就绪                                               │
└────────────────────────────────────────────────────────────┘
```

### 2. 智能体创建与网络构建流程

```
┌────────────────────────────────────────────────────────────┐
│  1. 创建智能体实例                                         │
│  agent = Agent("Agent_ID")                                 │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. 加载预定义知识库 (可选)                                │
│  - 从 datasets.py 加载专业领域知识                         │
│  - 调用 agent.learn() 方法学习知识                         │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. 建立智能体关系网络                                     │
│  - 调用 agent.connect(target_id, weight)                   │
│  - 关系存储在拓扑数据库中                                 │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. 验证关系网络                                           │
│  - 调用 agent.get_neighbors() 检查关系                     │
└────────────────────────────────────────────────────────────┘
```

### 3. 涟漪搜索算法执行流程

```
┌────────────────────────────────────────────────────────────┐
│  1. 接收查询请求                                           │
│  results = agent.ask(question, limit)                      │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. 查询文本向量化                                         │
│  - 使用 SentenceTransformers 生成向量                      │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. 获取智能体邻居列表                                     │
│  - 从拓扑数据库读取关系权重                               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. 邻居分组 (基于信任阈值)                                │
│  - 高信任组 (A组): 权重 ≥ high_trust_threshold            │
│  - 低信任组 (B组): 权重 ≥ low_trust_threshold 且 < high_trust_threshold │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. 第一轮搜索: 高信任组 + 自身                            │
│  - 查询A组智能体和自身的向量数据库                        │
│  - 收集相似度得分最高的结果                               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. 结果置信度评估                                         │
│  - 检查最高得分是否 ≥ high_confidence_threshold           │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────┴────────────────┐     ┌─────────────────────────┐
│  是: 返回结果              │     │  否: 第二轮搜索         │
│  - 排序并返回top-N结果     │     │  - 查询B组智能体的向量数据库 │
└────────────────────────────┘     └───────────┬─────────────┘
                                               │
┌───────────────────────────────────────────────▼─────────────┐
│  7. 合并结果并排序                                         │
│  - 合并两轮搜索结果                                        │
│  - 按相似度得分降序排列                                    │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  8. 返回最终结果                                           │
│  - 返回 SearchResult 列表                                  │
└────────────────────────────────────────────────────────────┘
```

### 4. 反馈机制执行流程

```
┌────────────────────────────────────────────────────────────┐
│  1. 接收反馈请求                                           │
│  agent.feedback(target_id, is_useful=True)                │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. 确定反馈类型                                           │
│  - positive: is_useful=True                                │
│  - negative: is_useful=False                               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. 获取当前关系权重                                       │
│  - 从拓扑数据库读取当前权重值                             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. 计算新权重值                                           │
│  - 基于反馈类型调整权重                                   │
│  - 确保权重在 [0, 1] 范围内                               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. 更新拓扑数据库                                         │
│  - 将新权重写入拓扑数据库                                 │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. 返回更新结果                                           │
│  - 返回新的权重值                                          │
└────────────────────────────────────────────────────────────┘
```

### 5. 完整系统调用示例流程

```
┌────────────────────────────────────────────────────────────┐
│  1. 启动服务                                               │
│  ./start_test_databases.sh                                 │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. 导入依赖                                               │
│  from synapse.api import Agent                             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. 创建智能体                                             │
│  finance_agent = Agent("Finance_Bot")                      │
│  market_agent = Agent("Market_Analyst")                    │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. 建立智能体连接                                         │
│  finance_agent.connect("Market_Analyst", 0.9)             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. 学习知识                                               │
│  finance_agent.learn("苹果公司2024年Q1营收增长10%")        │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. 执行检索                                               │
│  results = finance_agent.ask("苹果股票表现如何？", limit=3) │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  7. 处理检索结果                                           │
│  - 遍历结果列表                                            │
│  - 提取内容、来源、相似度得分                              │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  8. 提供反馈                                               │
│  finance_agent.feedback("Market_Analyst", is_useful=True) │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  9. 验证权重更新                                           │
│  neighbors = finance_agent.get_neighbors()                 │
└────────────────────────────────────────────────────────────┘
```

## 项目特点

1. **创新性**：突破传统检索模式，采用多智能体协作和涟漪搜索
2. **灵活性**：支持多种数据库后端，可根据需求灵活切换
3. **可扩展性**：易于添加新的智能体和扩展新的功能模块
4. **自适应性**：通过反馈机制不断优化，持续进化
5. **专业性**：针对不同领域设计智能体，提供专业知识检索

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

---

项目地址：https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse.git
联系人：ykd1374991239@163.com
</div>