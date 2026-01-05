'''Descripttion: 
version: 1.3
Author: YaoKaiDi
Date: 2026-01-04 10:57:56
LastEditors: YaoKaiDi
LastEditTime: 2026-01-04 16:44:20
'''
import yaml
import redis
from typing import List, Optional
from synapse.core.db import VectorDBClient, TopologyClient
from synapse.core.retriever import RippleSearcher, SearchResult
from synapse.core.feedback import WeightManager
from synapse.utils import get_embedding


class Agent:
    def __init__(self, agent_id: str, config_path: str = 'config.yaml'):
        self.agent_id = agent_id
        self.config_path = config_path
        
        self.vector_client = VectorDBClient(config_path)
        self.topology_client = TopologyClient(config_path)
        self.ripple_searcher = RippleSearcher(config_path)
        self.weight_manager = WeightManager(config_path)
        
        # Redis client for profile storage
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        redis_config = config['redis']
        self.redis_client = redis.Redis(
            host=redis_config['host'],
            port=redis_config['port'],
            db=redis_config['db'],
            decode_responses=True
        )

    def _get_profile_key(self) -> str:
        return f"agent:profile:{self.agent_id}"

    def set_profile(self, description: str, keywords: List[str]):
        profile = {
            'description': description,
            'keywords': ','.join(keywords)
        }
        self.redis_client.hset(self._get_profile_key(), mapping=profile)
        return f"Profile set for {self.agent_id}"

    def get_profile(self) -> dict:
        profile = self.redis_client.hgetall(self._get_profile_key())
        if profile:
            profile['keywords'] = profile['keywords'].split(',') if profile.get('keywords') else []
        return profile or {"description": "No description available", "keywords": []}

    def connect(self, target_agent_id: str, weight: float = 0.5):
        self.topology_client.set_link(self.agent_id, target_agent_id, weight)
        return f"Connected to {target_agent_id} with weight {weight}"

    def learn(self, text: str, metadata: Optional[dict] = None):
        vector = get_embedding(text)
        point_id = self.vector_client.add_memory(
            content=text,
            vector=vector,
            owner_id=self.agent_id,
            metadata=metadata
        )
        return f"Learned: {text} (ID: {point_id})"

    def ask(self, question: str, limit: int = 10) -> List[SearchResult]:
        results = self.ripple_searcher.search(question, self.agent_id, limit)
        return results

    def ask_with_details(self, question: str, limit: int = 10) -> dict:
        details = self.ripple_searcher.search_with_details(question, self.agent_id, limit)
        return details

    def feedback(self, target_agent_id: str, is_useful: bool = True):
        feedback_type = 'positive' if is_useful else 'negative'
        new_weight = self.weight_manager.update_interaction(
            source=self.agent_id,
            target=target_agent_id,
            feedback_type=feedback_type
        )
        return f"Feedback given to {target_agent_id}. New weight: {new_weight}"

    def get_neighbors(self):
        return self.topology_client.get_neighbors(self.agent_id)

    def get_knowledge(self):
        return self.vector_client.get_all_memories(self.agent_id)

    def disconnect(self, target_agent_id: str):
        self.topology_client.remove_link(self.agent_id, target_agent_id)
        return f"Disconnected from {target_agent_id}"

    def __repr__(self):
        neighbors = self.get_neighbors()
        return f"Agent(id={self.agent_id}, neighbors={len(neighbors)})"
