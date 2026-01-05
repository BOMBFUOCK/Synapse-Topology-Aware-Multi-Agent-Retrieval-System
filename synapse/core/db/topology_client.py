import yaml
from typing import Dict, List
import redis


class TopologyClient:
    _instance = None

    def __new__(cls, config_path: str = 'config.yaml'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: str = 'config.yaml'):
        if hasattr(self, 'initialized'):
            return
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        redis_config = config['redis']
        self.client = redis.Redis(
            host=redis_config['host'],
            port=redis_config['port'],
            db=redis_config['db'],
            decode_responses=True
        )
        self.initialized = True

    def _get_key(self, source_id: str) -> str:
        return f"topology:{source_id}"

    def set_link(self, source_id: str, target_id: str, weight: float):
        key = self._get_key(source_id)
        self.client.hset(key, target_id, str(weight))

    def get_neighbors(self, source_id: str) -> Dict[str, float]:
        key = self._get_key(source_id)
        neighbors = self.client.hgetall(key)
        return {k: float(v) for k, v in neighbors.items()}

    def get_weight(self, source_id: str, target_id: str) -> float:
        key = self._get_key(source_id)
        weight = self.client.hget(key, target_id)
        return float(weight) if weight else 0.0

    def remove_link(self, source_id: str, target_id: str):
        key = self._get_key(source_id)
        self.client.hdel(key, target_id)

    def get_all_links(self) -> Dict[str, Dict[str, float]]:
        all_links = {}
        pattern = "topology:*"
        for key in self.client.scan_iter(match=pattern):
            source_id = key.replace("topology:", "")
            neighbors = self.client.hgetall(key)
            all_links[source_id] = {k: float(v) for k, v in neighbors.items()}
        return all_links

    def clear_all(self):
        pattern = "topology:*"
        for key in self.client.scan_iter(match=pattern):
            self.client.delete(key)
