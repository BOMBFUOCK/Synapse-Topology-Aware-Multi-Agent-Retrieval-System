<div align="center">
  <img src="https://img.shields.io/github/stars/BOMBFUOCK/Multi-Agent-RAG-Synapse?style=social" alt="GitHub Stars" />
  <img src="https://img.shields.io/github/forks/BOMBFUOCK/Multi-Agent-RAG-Synapse?style=social" alt="GitHub Forks" />
  <img src="https://img.shields.io/github/watchers/BOMBFUOCK/Multi-Agent-RAG-Synapse?style=social" alt="GitHub Watchers" />
  <img src="https://img.shields.io/github/issues/BOMBFUOCK/Multi-Agent-RAG-Synapse" alt="GitHub Issues" />
  <img src="https://img.shields.io/github/issues-closed/BOMBFUOCK/Multi-Agent-RAG-Synapse" alt="GitHub Closed Issues" />
</div>

<div align="center">
  <a href="README_CN.md">中文版本</a> | English Version
</div>

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

### 5. Agent Profile

- **Profile Information**: Each agent has a profile containing description and keywords
- **Profile Management**: Support setting and getting agent profiles
- **No Result Fallback**: When ripple search finds no relevant content, returns agent profiles
- **Improved User Experience**: Helps users understand agent expertise and knowledge scope

## Differences from Traditional Retrieval Models

| Traditional Retrieval Model | Synapse Multi-Agent Retrieval |
|------------------------------|-------------------------------|
| Single retrieval source, information silos | Multi-agent collaboration, information network |
| Fixed retrieval scope, no priority | Trust-based, hierarchical search |
| Static retrieval, no learning ability | Dynamic learning, continuous evolution |
| No feedback mechanism, fixed results | Feedback-based adjustment, result optimization |
| Single vector database dependency | Support for multiple database backends, flexible expansion |

## Technical Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                      Synapse System Architecture              │
├─────────┬─────────┬───────────────────────────────────────────┤
│  Agent  │         │  Core Components                          │
│  API    │         ├─────────────────────┬─────────────────────┤
│         │         │  Retrieval Engine   │  Data Storage       │
└─────────┴─────────┼─────────────────────┼─────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│                  Ripple Searcher                              │
└───────────────────────────────────────────────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│  VectorDBClient                     TopologyClient            │
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
  - `ask(question, limit)`: Perform ripple search
  - `ask_with_details(question, limit)`: Search with detailed process
  - `feedback(target_agent_id, is_useful)`: Feedback mechanism
  - `connect(target_agent_id, weight)`: Establish agent connection
  - `set_profile(description, keywords)`: Set agent profile (description and keywords)
  - `get_profile()`: Get agent profile information

### RippleSearcher

- **Search Strategy**: Trust-based hierarchical search
- **Search Process**:
  1. Convert query to vector
  2. Get source agent's neighbor list
  3. Divide into high-trust group (Group A) and low-trust group (Group B) by trust weight
  4. First round search: Query vector databases of Group A and self
  5. If result confidence is high, return directly; otherwise perform second round search
  6. Second round search: Query vector databases of Group B
  7. If any results found, merge and return sorted results
  8. If no results found, return agent profiles containing description and keywords

### Dynamic Weight Management

- **Feedback-based Adjustment**: Positive feedback increases trust weight, negative feedback decreases
- **Adaptive Learning**: System continuously optimizes agent relationship network based on interaction history
- **Weight Range**: 0-1, 0 means no trust, 1 means complete trust

## Dataset Description

The system provides professional domain knowledge bases for each agent, including:

- Finance_Bot: Financial domain knowledge (15 items)
- Market_Analyst: Market analysis knowledge (15 items)
- News_Bot: News domain knowledge (15 items)
- Tech_Expert: Technical expert knowledge (15 items)
- Economic_Analyst: Economic analysis knowledge (15 items)

## Database Support

### Vector Databases

1. Qdrant


### Topology/Graph Databases

1. Redis


### Trace Chain Storage

#### Core Concepts

**Information-centric trace chain recording** is one of the system's core design principles, with the following key ideas:

- **Information-centric**: Treat each piece of information as an independent entity throughout its lifecycle
- **Complete tracking**: Record the full path of information from creation to propagation
- **Observability**: Provide visualization of information flow in the agent network
- **Auditability**: Support tracing the source and propagation history of information

The value of this design lies in:
- Improved system observability for debugging and optimization
- Support for information propagation analysis to identify key nodes in the network
- Audit capabilities ensuring information source traceability
- Support for information flow analysis in complex scenarios

#### Implementation Details

The system implements information-centric trace chain storage in Redis, capturing the complete propagation path of each piece of information:

**Data Structure:**

- **Key Format**: `info:trace:{info_id}`
- **Type**: Redis List
- **Content**: Stores information content in chronological order
- **Example**:
  ```
  RPUSH info:trace:uuid-123 "Microsoft acquired a startup..."
  RPUSH info:trace:uuid-123 "Microsoft acquired a startup..." (second propagation)
  ```

**Information ID Generation:**

- Generated using UUID v4 when `learn()` is called
- Stored as metadata in vector database
- Returned with search results

**Trace Recording Flow:**

1. User/Agent A initiates search request
2. RippleSearcher queries vector database
3. Gets search results containing `info_id` and `content`
4. Appends `content` to Redis List: `info:trace:{info_id}`
5. Returns results to user/Agent A

**Query Examples:**

```python
# Get complete propagation path for specific information
trace = redis_client.lrange("info:trace:uuid-1234", 0, -1)

# Get propagation path length
length = redis_client.llen("info:trace:uuid-1234")

# Get latest 5 propagation records
latest = redis_client.lrange("info:trace:uuid-1234", -5, -1)
```

**Trace Management Tools:**

- `InfoTraceManager`: Provides trace query and management functionality
- `get_trace(info_id)`: Get complete propagation path
- `get_trace_length(info_id)`: Get propagation count
- `print_trace_info(info_id)`: Print formatted trace information

#### Implementation Architecture

The implementation architecture of trace chain storage is closely integrated with other system components:

```
┌───────────────────────────────────────────────────────────────┐
│                      System Architecture                    │
├─────────┬─────────┬───────────────────────────────────────────┤
│  Agent  │         │  Core Components                          │
│  API    │         ├─────────────────────┬─────────────────────┤
│         │         │  Retrieval Engine   │  Data Storage       │
└─────────┴─────────┼─────────────────────┼─────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│                  RippleSearcher                              │
└───────────────────────────────────────────────────────────────┘
                    │  ▲                 │  ▲
                    │  │                 │  │
                    ▼  │                 ▼  │
┌───────────────────────────────────────────────────────────────┐
│  VectorDBClient                     TopologyClient            │
│  └─── Add info_id generation and storage   │  └─── Manage agent relationship network     │
└───────────────────────────────────────────────────────────────┘
                    │                      │
                    ▼                      ▼
┌─────────────────────────┐    ┌───────────────────────────┐
│  Vector Database        │    │  Redis Topology Database  │
│  Store content and info_id │    │  Store agent relations and trace chains  │
└─────────────────────────┘    └───────────────────────────┘
```

**Technology Selection Considerations:**

- **Redis List**: Redis List is chosen as the storage structure because it naturally supports appending elements in chronological order, suitable for recording propagation paths
- **UUID**: UUID is used as the information ID to ensure global uniqueness
- **Integrated Design**: Closely integrated with the existing system, no additional storage services required

#### Code Implementation Points

**Key Code Locations:**

1. **Vector Database Client** (`synapse/core/db/vector_client.py`):
   - Generate and store `info_id`
   - Implement trace recording and query methods

2. **Ripple Searcher** (`synapse/core/retriever/ripple_search.py`):
   - Record trace chain before returning search results
   - Ensure `info_id` is passed to final results

3. **Agent API** (`synapse/api.py`):
   - Expose trace chain query interfaces
   - Integrate trace management functionality

4. **Trace Management Tools** (`synapse/utils/trace_manager.py`):
   - Provide advanced query and visualization features

**Important Design Decisions:**

- **Lazy Loading**: Trace chain recording is performed asynchronously after search completion, without affecting search performance
- **Data Compression**: For duplicate content, only references are recorded instead of complete content (current implementation uses complete content, can be optimized as needed)
- **Extensible Design**: Supports adding more complex trace chain analysis features in the future

#### Application Scenarios and Value

The trace chain storage feature has important value in various scenarios:

##### 1. System Debugging and Optimization

- **Issue Localization**: When the system encounters exceptions or returns incorrect results, the propagation path can be traced to identify the source and process
- **Performance Optimization**: Analyze information propagation paths to identify bottlenecks and inefficient nodes in the network
- **Debugging Assistance**: Provide complete information flow paths for developers to debug complex agent interactions

##### 2. Information Propagation Analysis

- **Propagation Scope Analysis**: Understand the breadth and depth of information propagation in the agent network
- **Key Node Identification**: Discover the most active information propagation nodes in the network
- **Propagation Pattern Discovery**: Analyze patterns and规律 of information propagation

##### 3. Audit and Compliance

- **Source Tracing**: Ensure each piece of information's source is traceable, meeting compliance requirements
- **Propagation Audit**: Record complete information propagation history to support audit needs
- **Responsibility Tracing**: In case of issues, trace to relevant agents and propagation paths

##### 4. Complex Scenario Support

- **Multi-turn Dialogue**: Support information flow analysis in multi-turn dialogue scenarios
- **Cross-agent Collaboration**: Support information tracking in complex collaboration scenarios
- **Dynamic Network**: Adapt to dynamic changes in the agent network

##### 5. Agent Network Optimization

- **Relationship Network Adjustment**: Optimize trust relationships between agents based on trace analysis results
- **Agent Capability Evaluation**: Evaluate agent performance and value based on information propagation effects
- **Network Topology Optimization**: Optimize agent network topology based on trace analysis


## Quick Start

### Start Dependent Services

```bash
# Start required databases using Docker Compose
docker-compose up -d
```

### Run Example

```bash
# Install dependencies
./venv/bin/python3 -m pip install -r requirements.txt

# Install additional SOCKS support (required for Qdrant client)
./venv/bin/python3 -m pip install 'httpx[socks]'

# Run the main program
./venv/bin/python3 main.py
```

### Basic Usage

```python
from synapse.api import Agent

# Create agents
agent_a = Agent("Finance_Bot")
agent_b = Agent("Market_Analyst")

# Set agent profiles
agent_a.set_profile(
    description="Financial expert agent, specializing in analysis and advice on stocks, bonds, funds and other financial products.",
    keywords=["stocks", "bonds", "funds", "financial analysis", "investment advice"]
)

agent_b.set_profile(
    description="Market analyst agent, good at analyzing market trends, industry dynamics and company financial reports.",
    keywords=["market analysis", "industry dynamics", "company financial reports", "trend prediction", "data analysis"]
)

# Get agent profile
profile = agent_a.get_profile()
print(f"Agent Profile: {profile}")

# Establish connection
agent_a.connect("Market_Analyst", 0.9)

# Learn knowledge
agent_a.learn("Apple Inc. Q1 2024 revenue increased by 10%")

# Perform search
results = agent_a.ask("How is Apple's stock performing?", limit=3)

# When no results found, returns agent profiles
test_results = agent_a.ask("This is a test question with no matching results", limit=3)

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
│  2. Load Configuration File (config.yaml)                 │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Initialize Database Clients                           │
│  - Vector Database Client (VectorDBClient)                │
│  - Topology Database Client (TopologyClient)              │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Initialize Retrieval Engine (RippleSearcher)         │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. Initialize Weight Manager (WeightManager)            │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. System Ready                                          │
└────────────────────────────────────────────────────────────┘
```

### 2. Agent Creation and Network Construction Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Create Agent Instance                                 │
│  agent = Agent("Agent_ID")                                │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Load Predefined Knowledge Base (Optional)             │
│  - Load professional domain knowledge from datasets.py    │
│  - Call agent.learn() method to learn knowledge           │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Build Agent Relationship Network                      │
│  - Call agent.connect(target_id, weight)                  │
│  - Relationships stored in topology database              │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Verify Relationship Network                           │
│  - Call agent.get_neighbors() to check relationships      │
└────────────────────────────────────────────────────────────┘
```

### 3. Ripple Search Algorithm Execution Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Receive Query Request                                 │
│  results = agent.ask(question, limit)                     │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Query Text Vectorization                              │
│  - Generate vector using SentenceTransformers             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Get Agent Neighbor List                               │
│  - Read relationship weights from topology database       │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Neighbor Grouping (Based on Trust Threshold)          │
│  - High Trust Group (Group A): Weight ≥ high_trust_threshold │
│  - Low Trust Group (Group B): Weight ≥ low_trust_threshold and < high_trust_threshold │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. First Round Search: High Trust Group + Self           │
│  - Query vector databases of Group A agents and self      │
│  - Collect results with highest similarity scores         │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. Result Confidence Evaluation                          │
│  - Check if highest score ≥ high_confidence_threshold     │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────┴────────────────┐     ┌─────────────────────────┐
│  Yes: Return Results       │     │  No: Second Round Search│
│  - Sort and return top-N results │  - Query vector databases of Group B agents │
└────────────────────────────┘     └───────────┬─────────────┘
                                               │
┌───────────────────────────────────────────────▼─────────────┐
│  7. Merge Results and Check                               │
│  - Merge results from both rounds                         │
│  - Check if any results found                             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────┴────────────────┐     ┌─────────────────────────┐
│  Yes: Sort Results         │     │  No: Return Agent Profiles│
│  - Sort by similarity score in descending order │  - Get all agent IDs     │
│  - Return top-N results                       │  - Query agent profiles   │
│                                               │  - Return profile information │
└───────────┬────────────────┘     └───────────┬─────────────┘
            │                                   │
┌───────────▼───────────────────────────────────▼─────────────┐
│  8. Return Final Results                                  │
│  - Return SearchResult list or agent profiles             │
└────────────────────────────────────────────────────────────┘
```

### 4. Feedback Mechanism Execution Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Receive Feedback Request                              │
│  agent.feedback(target_id, is_useful=True)               │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Determine Feedback Type                               │
│  - positive: is_useful=True                               │
│  - negative: is_useful=False                              │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Get Current Relationship Weight                       │
│  - Read current weight value from topology database       │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Calculate New Weight Value                            │
│  - Adjust weight based on feedback type                   │
│  - Ensure weight is within [0, 1] range                   │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. Update Topology Database                              │
│  - Write new weight to topology database                  │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. Return Update Result                                  │
│  - Return new weight value                                │
└────────────────────────────────────────────────────────────┘
```

### 5. Complete System Call Example Flow

```
┌────────────────────────────────────────────────────────────┐
│  1. Start Services                                         │
│  docker-compose up -d                                     │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  2. Import Dependencies                                    │
│  from synapse.api import Agent                             │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  3. Create Agents                                          │
│  finance_agent = Agent("Finance_Bot")                     │
│  market_agent = Agent("Market_Analyst")                   │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  4. Establish Agent Connections                           │
│  finance_agent.connect("Market_Analyst", 0.9)            │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  5. Learn Knowledge                                        │
│  finance_agent.learn("Apple Inc. Q1 2024 revenue increased by 10%") │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  6. Perform Retrieval                                      │
│  results = finance_agent.ask("How is Apple's stock performing?", limit=3) │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  7. Process Retrieval Results                              │
│  - Iterate through results list                           │
│  - Extract content, source, similarity score              │
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

1. **Innovation**: Breaks through traditional retrieval models, adopting multi-agent collaboration and ripple search
2. **Flexibility**: Supports multiple database backends, can be flexibly switched according to needs
3. **Scalability**: Easy to add new agents and extend new functional modules
4. **Adaptability**: Continuously optimized through feedback mechanisms, constantly evolving
5. **Professionalism**: Designed for different fields, providing professional knowledge retrieval

## Application Scenarios

1. **Professional Domain Knowledge Retrieval**: Deep knowledge retrieval in finance, healthcare, legal and other professional fields
2. **Distributed Information Systems**: Enterprise internal multi-department information sharing and retrieval
3. **Intelligent Assistant Networks**: Build intelligent assistant collaboration networks, providing more comprehensive services
4. **Knowledge Graph Expansion**: Dynamically expand and optimize knowledge graphs
5. **Decision Support Systems**: Provide multi-source information support for complex decisions

## Project Structure

```
synapse/
├── main.py              # Main program, demonstrating system functionality
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
├── docker-compose.yml   # Docker configuration for required databases
└── requirements.txt     # Project dependencies
```

## Testing Framework

The system includes a built-in test mechanism in `main.py` that demonstrates:

- Agent creation and network construction
- Knowledge learning and storage
- Ripple search functionality
- Feedback mechanism and dynamic weight adjustment
- Multi-round retrieval and result evaluation

## Future Outlook

1. **Agent Auto-generation**: Automatically generate professional domain agents based on requirements
2. **More Complex Trust Models**: Introduce multi-dimensional trust evaluation
3. **Real-time Data Updates**: Support real-time knowledge updates from external data sources
4. **Visual Interface**: Provide visualization of agent networks and search processes
5. **Multi-language Support**: Expand to multi-language environments

## Summary

The Synapse Multi-Agent Information Retrieval System achieves more efficient and intelligent information retrieval than traditional retrieval models through its innovative ripple search algorithm and dynamic trust relationship network. The system has good scalability and adaptability, and can be widely applied in various professional fields and complex information retrieval scenarios.

---

## Star History

<div align="center">
  <a href="https://star-history.com/#BOMBFUOCK/Multi-Agent-RAG-Synapse&Date">
    <img src="https://api.star-history.com/svg?repos=BOMBFUOCK/Multi-Agent-RAG-Synapse&type=Date" alt="Star History Chart" width="800" height="800">
  </a>
</div>

## Contributors

<div align="center">
  <a href="https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=BOMBFUOCK/Multi-Agent-RAG-Synapse" alt="Contributors" />
  </a>
</div>

---

Project Address: https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse.git
Contact: ykd1374991239@163.com
