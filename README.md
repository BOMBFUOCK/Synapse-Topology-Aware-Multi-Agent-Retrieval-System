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

### RippleSearcher

- **Search Strategy**: Trust-based hierarchical search
- **Search Process**:
  1. Convert query to vector
  2. Get source agent's neighbor list
  3. Divide into high-trust group (Group A) and low-trust group (Group B) by trust weight
  4. First round search: Query vector databases of Group A and self
  5. If result confidence is high, return directly; otherwise perform second round search
  6. Second round search: Query vector databases of Group B
  7. Merge results and return sorted

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
# Start all test databases using Docker Compose
./start_test_databases.sh
```

### Run Example

```bash
# Install dependencies
pip install -r requirements.txt

# Run the main program
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
agent_a.learn("Apple Inc. Q1 2024 revenue increased by 10%")

# Perform search
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
│  7. Merge Results and Sort                                │
│  - Merge results from both rounds                         │
│  - Sort by similarity score in descending order           │
└───────────┬────────────────────────────────────────────────┘
            │
┌───────────▼────────────────────────────────────────────────┐
│  8. Return Final Results                                  │
│  - Return SearchResult list                               │
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
│  ./start_test_databases.sh                                │
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
syn/
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
├── test_databases.py    # Database test script
├── docker-compose-all-dbs.yml  # Docker configuration for all databases
├── start_test_databases.sh     # Script to start test databases
└── requirements.txt     # Project dependencies
```

## Testing Framework

The system provides a complete database testing framework:

- Supports performance testing of 8 different databases
- Test metrics include: vector query time, relationship query time, storage efficiency, etc.
- Provides detailed test reports and comparative analysis

## Future Outlook

1. **Agent Auto-generation**: Automatically generate professional domain agents based on requirements
2. **More Complex Trust Models**: Introduce multi-dimensional trust evaluation
3. **Real-time Data Updates**: Support real-time knowledge updates from external data sources
4. **Visual Interface**: Provide visualization of agent networks and search processes
5. **Multi-language Support**: Expand to multi-language environments

## Summary

The Synapse Multi-Agent Information Retrieval System achieves more efficient and intelligent information retrieval than traditional retrieval models through its innovative ripple search algorithm and dynamic trust relationship network. The system has good scalability and adaptability, and can be widely applied in various professional fields and complex information retrieval scenarios.

---

Project Address: https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse.git
Contact: ykd1374991239@163.com
