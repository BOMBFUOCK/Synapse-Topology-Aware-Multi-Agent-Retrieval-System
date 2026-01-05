import yaml
from typing import List, Optional
from dataclasses import dataclass
from synapse.core.db import VectorDBClient, TopologyClient
from synapse.utils import get_embedding


@dataclass
class SearchResult:
    content: str
    source_agent_id: str
    score: float
    metadata: dict = None


class RippleSearcher:
    def __init__(self, config_path: str = 'config.yaml'):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.vector_client = VectorDBClient(config_path)
        self.topology_client = TopologyClient(config_path)
        
        retrieval_config = config['retrieval']
        self.high_trust_threshold = retrieval_config['high_trust_threshold']
        self.low_trust_threshold = retrieval_config['low_trust_threshold']
        self.high_confidence_threshold = retrieval_config['high_confidence_threshold']
        self.default_limit = retrieval_config['default_limit']

    def search(self, query_text: str, source_agent_id: str, limit: Optional[int] = None) -> List[SearchResult]:
        limit = limit or self.default_limit
        query_vector = get_embedding(query_text)
        
        neighbors = self.topology_client.get_neighbors(source_agent_id)
        
        group_a = []
        group_b = []
        
        for neighbor_id, weight in neighbors.items():
            if weight >= self.high_trust_threshold:
                group_a.append(neighbor_id)
            elif weight >= self.low_trust_threshold:
                group_b.append(neighbor_id)
        
        first_round_ids = group_a + [source_agent_id]
        
        if first_round_ids:
            results = self.vector_client.query_memory(query_vector, first_round_ids, limit)
            if results and results[0]['score'] >= self.high_confidence_threshold:
                return [SearchResult(
                    content=r['content'],
                    source_agent_id=r['owner_id'],
                    score=r['score'],
                    metadata=r.get('metadata')
                ) for r in results]
        
        if group_b:
            results = self.vector_client.query_memory(query_vector, group_b, limit)
            return [SearchResult(
                content=r['content'],
                source_agent_id=r['owner_id'],
                score=r['score'],
                metadata=r.get('metadata')
            ) for r in results]
        
        return []

    def search_with_details(self, query_text: str, source_agent_id: str, limit: Optional[int] = None) -> dict:
        limit = limit or self.default_limit
        query_vector = get_embedding(query_text)
        
        neighbors = self.topology_client.get_neighbors(source_agent_id)
        
        group_a = []
        group_b = []
        
        for neighbor_id, weight in neighbors.items():
            if weight >= self.high_trust_threshold:
                group_a.append(neighbor_id)
            elif weight >= self.low_trust_threshold:
                group_b.append(neighbor_id)
        
        details = {
            'source_agent_id': source_agent_id,
            'neighbors': neighbors,
            'group_a_high_trust': group_a,
            'group_b_low_trust': group_b,
            'round': None,
            'results': []
        }
        
        first_round_ids = group_a + [source_agent_id]
        
        if first_round_ids:
            results = self.vector_client.query_memory(query_vector, first_round_ids, limit)
            details['round'] = 1
            details['searched_ids'] = first_round_ids
            if results and results[0]['score'] >= self.high_confidence_threshold:
                details['results'] = [SearchResult(
                    content=r['content'],
                    source_agent_id=r['owner_id'],
                    score=r['score'],
                    metadata=r.get('metadata')
                ) for r in results]
                return details
        
        if group_b:
            results = self.vector_client.query_memory(query_vector, group_b, limit)
            details['round'] = 2
            details['searched_ids'] = group_b
            details['results'] = [SearchResult(
                content=r['content'],
                source_agent_id=r['owner_id'],
                score=r['score'],
                metadata=r.get('metadata')
            ) for r in results]
            return details
        
        details['searched_ids'] = []
        return details
