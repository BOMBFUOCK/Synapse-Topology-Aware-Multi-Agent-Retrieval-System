<div align="center">
  <a href="README_CN.md" style="padding: 8px 16px; margin: 0 8px; background-color: #2563eb; color: white; border-radius: 4px; text-decoration: none;">中文</a>
  <a href="#" style="padding: 8px 16px; margin: 0 8px; background-color: #f3f4f6; color: #374151; border: 1px solid #e5e7eb; border-radius: 4px; text-decoration: none;">English</a>
</div>

<div align="center">
  <img src="https://img.shields.io/github/stars/BOMBFUOCK/Multi-Agent-RAG-Synapse?style=social" alt="GitHub Stars" />
  <img src="https://img.shields.io/github/forks/BOMBFUOCK/Multi-Agent-RAG-Synapse?style=social" alt="GitHub Forks" />
  <img src="https://img.shields.io/github/watchers/BOMBFUOCK/Multi-Agent-RAG-Synapse?style=social" alt="GitHub Watchers" />
  <img src="https://img.shields.io/github/issues/BOMBFUOCK/Multi-Agent-RAG-Synapse" alt="GitHub Issues" />
  <img src="https://img.shields.io/github/issues-closed/BOMBFUOCK/Multi-Agent-RAG-Synapse" alt="GitHub Closed Issues" />
</div>

<div align="center">
  <a href="https://star-history.com/#BOMBFUOCK/Multi-Agent-RAG-Synapse&Date">
    <img src="https://api.star-history.com/svg?repos=BOMBFUOCK/Multi-Agent-RAG-Synapse&type=Date" alt="Star History Chart" width="800" height="800">
  </a>
</div>

<hr>

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

## System Architecture

### 1. Agent Model
- **Agent Class**: Represents a single agent, containing attributes like id, name, domain, knowledge vector, etc.
- **Relationship Class**: Represents trust relationships between agents, containing source agent, target agent, trust weight, etc.

### 2. Retrieval Process
1. **Initial Retrieval**: User initiates a retrieval request through the main agent
2. **Ripple Diffusion**: Main agent diffuses the request to its trusted neighbors
3. **Result Collection**: Collect retrieval results from all agents
4. **Result Filtering**: Filter most relevant results based on similarity scores
5. **Result Return**: Return final results to the user
6. **Feedback Learning**: Adjust trust weights between agents based on user feedback

### 3. Database Model
- **Vector Database**:
  - Table structure: agent_id, knowledge_vector, metadata
  - Supports vector similarity queries
- **Topology Database**:
  - Table structure: source_agent_id, target_agent_id, trust_weight, last_updated
  - Supports graph queries to quickly find an agent's neighbors

## Quick Start

### 1. Environment Setup
- Python 3.8+
- Install dependencies: `pip install -r requirements.txt`

### 2. Start Databases
- Start test databases with Docker: `bash start_test_databases.sh`
- Or manually configure vector and topology databases

### 3. Run Example
```python
from synapse.api import Agent, Synapse

# Create Synapse instance
synapse = Synapse()

# Create agents
agent1 = Agent(id="Finance_Bot", name="Finance Bot", domain="Finance")
agent2 = Agent(id="Market_Analyst", name="Market Analyst", domain="Market Analysis")
agent3 = Agent(id="News_Bot", name="News Bot", domain="News")

# Add agents to the system
synapse.add_agent(agent1)
synapse.add_agent(agent2)
synapse.add_agent(agent3)

# Establish trust relationships between agents
synapse.add_relationship("Finance_Bot", "Market_Analyst", 0.8)
synapse.add_relationship("Market_Analyst", "News_Bot", 0.7)

# Agents learn knowledge
agent1.learn(["Global economic growth is expected to be 3.1% in 2024"])
agent2.learn(["Technology stocks rose 25% in the past year"])
agent3.learn(["The Federal Reserve decided to keep interest rates unchanged"])

# Perform retrieval
results = synapse.retrieve("Finance_Bot", "2024 economic trends")
print(results)
```

### 4. API Reference

#### Agent Class
```python
class Agent:
    def __init__(self, id, name, domain):
        # Initialize agent
        pass
    
    def learn(self, knowledge_items):
        # Learn new knowledge
        pass
    
    def retrieve(self, query):
        # Retrieve knowledge
        pass
```

#### Synapse Class
```python
class Synapse:
    def __init__(self):
        # Initialize system
        pass
    
    def add_agent(self, agent):
        # Add agent
        pass
    
    def add_relationship(self, source_agent_id, target_agent_id, trust_weight):
        # Add agent relationship
        pass
    
    def retrieve(self, main_agent_id, query, high_trust_threshold=0.7, low_trust_threshold=0.3, max_rounds=2, max_results=5):
        # Perform ripple retrieval
        pass
```

## Application Scenarios

1. **Professional Domain Knowledge Retrieval**: Deep knowledge retrieval in finance, healthcare, legal and other professional fields
2. **Distributed Information Systems**: Enterprise internal multi-department information sharing and retrieval
3. **Intelligent Assistant Networks**: Building intelligent assistant collaboration networks to provide more comprehensive services
4. **Knowledge Graph Expansion**: Dynamic expansion and optimization of knowledge graphs
5. **Decision Support Systems**: Providing multi-source information support for complex decisions

## Project Structure

```
syn/
├── main.py              # Main program demonstrating system functionality
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

## Contributors

<div align="center">
  <a href="https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=BOMBFUOCK/Multi-Agent-RAG-Synapse" alt="Contributors" />
  </a>
</div>

---

Project Address: https://github.com/BOMBFUOCK/Multi-Agent-RAG-Synapse.git
Contact: ykd1374991239@163.com
