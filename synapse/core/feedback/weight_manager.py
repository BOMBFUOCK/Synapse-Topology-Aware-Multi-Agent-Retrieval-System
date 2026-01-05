import yaml
from typing import List
from synapse.core.db import TopologyClient


class WeightManager:
    def __init__(self, config_path: str = 'config.yaml'):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        self.topology_client = TopologyClient(config_path)
        
        weight_config = config['weight']
        retrieval_config = config['retrieval']
        
        self.positive_increment = weight_config['positive_increment']
        self.negative_decrement = weight_config['negative_decrement']
        self.decay_rate = weight_config['decay_rate']
        self.min_weight = weight_config['min_weight']
        self.max_weight = weight_config['max_weight']
        self.low_trust_threshold = retrieval_config['low_trust_threshold']

    def update_interaction(self, source: str, target: str, feedback_type: str):
        current_weight = self.topology_client.get_weight(source, target)
        
        if feedback_type == 'positive':
            new_weight = current_weight + self.positive_increment
        elif feedback_type == 'negative':
            new_weight = current_weight - self.negative_decrement
        else:
            raise ValueError(f"Invalid feedback_type: {feedback_type}. Must be 'positive' or 'negative'")
        
        new_weight = max(self.min_weight, min(self.max_weight, new_weight))
        
        if new_weight > 0:
            self.topology_client.set_link(source, target, new_weight)
        else:
            self.topology_client.remove_link(source, target)
        
        return new_weight

    def apply_decay(self, decay_rate: float = None):
        decay_rate = decay_rate or self.decay_rate
        all_links = self.topology_client.get_all_links()
        
        for source_id, neighbors in all_links.items():
            for target_id, weight in neighbors.items():
                new_weight = weight * decay_rate
                if new_weight >= self.low_trust_threshold:
                    self.topology_client.set_link(source_id, target_id, new_weight)
                else:
                    self.topology_client.remove_link(source_id, target_id)
        
        return all_links

    def batch_update(self, updates: List[tuple]):
        results = []
        for source, target, feedback_type in updates:
            new_weight = self.update_interaction(source, target, feedback_type)
            results.append({
                'source': source,
                'target': target,
                'feedback_type': feedback_type,
                'new_weight': new_weight
            })
        return results
