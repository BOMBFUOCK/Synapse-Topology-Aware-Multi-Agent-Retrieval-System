这份文档是专门为指导开发（无论是通过 Trea 这样的 AI 还是人类工程师）而设计的 **“Synapse 开发指令书” (Master Development Directive)**。

它将抽象的架构图转化为具体的**文件结构**、**代码任务**和**验收标准**。你可以直接把这份文档发给 Trea，或者分阶段喂给它。

---

# Synapse 项目开发指令书 (Master Development Directive)

## 0. 项目背景与目标

我们要开发 **Synapse**，一个基于 Python 的多智能体信息检索系统。
**核心原则**：

1. **双存储**：向量库存数据，Redis 存关系权重。
2. **涟漪检索**：优先查强关系（高权重），查不到再查弱关系。
3. **动态权重**：权重根据反馈实时更新，并随时间衰减。

---

## 1. 技术栈规范 (Tech Stack)

* **语言**: Python 3.9+
* **向量数据库**: Qdrant (使用 `qdrant-client`, 优先 Docker 部署)
* **拓扑/缓存**: Redis (使用 `redis-py`, 存 Sorted Sets)
* **Embedding**: `sentence-transformers` (本地开发用 `all-MiniLM-L6-v2`) 或 OpenAI API
* **配置管理**: `PyYAML`

---

## 2. 推荐的项目文件结构 (Project Structure)

请按照以下结构初始化项目：

```text
synapse/
├── config.yaml              # 数据库连接与阈值配置
├── main.py                  # 示例运行脚本
├── requirements.txt         # 依赖列表
└── synapse/
    ├── __init__.py
    ├── api.py               # 用户接口 (Agent类)
    ├── core/
    │   ├── __init__.py
    │   ├── db/
    │   │   ├── __init__.py
    │   │   ├── vector_client.py  # Qdrant 封装
    │   │   └── topology_client.py # Redis 封装
    │   ├── retriever/
    │   │   ├── __init__.py
    │   │   └── ripple_search.py  # 核心检索逻辑 (分层)
    │   └── feedback/
    │   │   ├── __init__.py
    │   │   └── weight_manager.py # 权重计算与衰减
    └── utils/
        └── embedding.py     # Embedding 模型封装

```

---

## 3. 分阶段开发任务 (Step-by-Step Instructions)

请按顺序执行以下四个阶段的开发。

### 第一阶段：基础设施层 (Infrastructure Layer)

**目标**：打通底层存储，能够写入向量和设置关系。

* **Task 1.1: 配置与工具**
* 创建 `config.yaml`，定义 Redis 和 Qdrant 的 host/port。
* 在 `synapse/utils/embedding.py` 中实现一个简单的 `get_embedding(text)` 函数。


* **Task 1.2: 向量库客户端 (`vector_client.py`)**
* 实现类 `VectorDBClient`。
* 方法 `add_memory(content, vector, owner_id, metadata)`。
* 方法 `query_memory(query_vector, owner_id_list, limit)`。**注意**：必须支持通过 `owner_id` 列表进行 Filter。


* **Task 1.3: 拓扑客户端 (`topology_client.py`)**
* 实现类 `TopologyClient`。
* 方法 `set_link(source_id, target_id, weight)`：使用 Redis ZADD。
* 方法 `get_neighbors(source_id)`：返回 `{neighbor_id: weight}` 字典。



> **✅ 阶段验收标准**：写一个脚本，能向 Qdrant 存入一条带 owner_id 的数据，并能在 Redis 中读出 Agent A 到 Agent B 的权重。

---

### 第二阶段：核心检索引擎 (Ripple Retrieval Engine)

**目标**：实现“由近及远”的检索逻辑。

* **Task 2.1: 涟漪逻辑 (`ripple_search.py`)**
* 实现类 `RippleSearcher`。
* **逻辑流程**：
1. 接收 `query_text` 和 `source_agent_id`。
2. 调用 `TopologyClient` 获取邻居。
3. 将邻居分为两组：
* `Group_A` (High Trust): Weight >= 0.8 (配置读取)
* `Group_B` (Low Trust): 0.3 <= Weight < 0.8


4. **第1轮检索**：调用 `VectorDBClient`，Filter 限定为 `Group_A` + 自身。
* 若结果最高分 > 0.85 (High Confidence)，直接返回。


5. **第2轮检索**：若第1轮失败，Filter 限定为 `Group_B`。




* **Task 2.2: 结果封装**
* 定义统一的返回对象 `SearchResult`，包含 `content`, `source_agent_id`, `score`。



> **✅ 阶段验收标准**：创建 Agent A, B, C。A-B 是强关系，A-C 是弱关系。
> * 测试1：A 问 B 知道的事 -> 返回 B 的数据（来源显示强关系）。
> * 测试2：A 问 C 知道的事 -> 只有当 B 不知道时，才返回 C 的数据。
> 
> 

---

### 第三阶段：动态权重系统 (Dynamic Weighting)

**目标**：让系统根据反馈变聪明。

* **Task 3.1: 权重管理器 (`weight_manager.py`)**
* 实现类 `WeightManager`。
* 方法 `update_interaction(source, target, feedback_type)`:
* `feedback_type="positive"` -> `weight += 0.05`
* `feedback_type="negative"` -> `weight -= 0.1`
* **约束**：权重必须限制在 0.0 到 1.0 之间。




* **Task 3.2: 衰减机制 (`decay_scheduler`)**
* 方法 `apply_decay(decay_rate=0.98)`:
* 遍历 Redis 中所有的 Key，将所有 Score 乘以 `0.98`。
* (注：开发阶段可写成一个手动调用的函数，暂不需要复杂的 Cron)。





> **✅ 阶段验收标准**：
> * 模拟 A 采纳了 C 的信息（调用一次 Positive Update）。
> * 检查 Redis，确认 A->C 的权重数值增加了。
> 
> 

---

### 第四阶段：API 封装与 SDK (User Interface)

**目标**：提供给开发者简单易用的接口。

* **Task 4.1: Agent 类 (`api.py`)**
* 初始化：`agent = Agent("Finance_Bot")`
* 方法 `connect(target_agent_name, weight)`: 建立关系。
* 方法 `learn(text)`: 将文本存入知识库。
* 方法 `ask(question)`: 执行涟漪检索。
* 方法 `feedback(target_agent_name, is_useful=True)`: 更新权重。


* **Task 4.2: 综合测试脚本 (`main.py`)**
* 编写一个完整的 Story：建立网络 -> 注入知识 -> 提问 -> 反馈 -> 再次提问（观察变化）。



---

## 4. 给 Trea 的提示词建议 (Prompt Guide)

你可以复制以下 Prompt 直接发给 Trea 开始工作：

**[Prompt 1: 初始化]**

> "Trea，我们要开发 Synapse 系统。请根据上面的【文件结构】部分，为我初始化项目目录，并生成 requirements.txt 和 config.yaml 文件。技术栈是 Python, Qdrant, Redis。"

**[Prompt 2: 第一阶段]**

> "现在开始开发 Core DB 层。请实现 `synapse/core/db/` 下的 `VectorDBClient` (基于 qdrant-client) 和 `TopologyClient` (基于 redis-py)。请确保 VectorClient 支持传入 `owner_id` 列表作为 filter 条件。"

**[Prompt 3: 第二阶段]**

> "接下来实现核心逻辑 `synapse/core/retriever/ripple_search.py`。请按照大纲中的【3.1 涟漪检索算法】实现分层检索逻辑。请务必实现：如果第一层（强关系）检索分数超过阈值，就直接返回，不进行第二层检索。"

**[Prompt 4: 第三阶段]**

> "现在实现动态权重。请在 `synapse/core/feedback/weight_manager.py` 中实现 `update_interaction` 函数，支持正向增强和负向惩罚，并确保权重在 0-1 之间。同时实现一个简单的衰减函数。"