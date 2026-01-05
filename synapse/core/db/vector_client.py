import yaml
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import uuid


class VectorDBClient:
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
        
        qdrant_config = config['qdrant']
        self.client = QdrantClient(
            host=qdrant_config['host'],
            port=qdrant_config['port']
        )
        self.collection_name = qdrant_config['collection_name']
        self.vector_size = 384
        
        self._ensure_collection()
        self.initialized = True

    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=Distance.COSINE)
            )

    def add_memory(self, content: str, vector: List[float], owner_id: str, metadata: Optional[Dict[str, Any]] = None):
        point_id = str(uuid.uuid4())
        
        payload = {
            'content': content,
            'owner_id': owner_id,
            **(metadata or {})
        }
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=point_id, vector=vector, payload=payload)]
        )
        return point_id

    def query_memory(self, query_vector: List[float], owner_id_list: List[str], limit: int = 10) -> List[Dict[str, Any]]:
        if not owner_id_list:
            return []
        
        should_conditions = [
            FieldCondition(
                key="owner_id",
                match=MatchValue(value=owner_id)
            )
            for owner_id in owner_id_list
        ]
        
        from qdrant_client.models import Filter as QdrantFilter
        query_filter = QdrantFilter(should=should_conditions)
        
        search_result = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit
        )
        
        results = []
        for hit in search_result.points:
            results.append({
                'content': hit.payload['content'],
                'owner_id': hit.payload['owner_id'],
                'score': hit.score,
                'metadata': {k: v for k, v in hit.payload.items() if k not in ['content', 'owner_id']}
            })
        
        return results

    def get_all_memories(self, owner_id: str) -> List[Dict[str, Any]]:
        from qdrant_client.models import Filter as QdrantFilter
        
        query_filter = QdrantFilter(
            must=[
                FieldCondition(
                    key="owner_id",
                    match=MatchValue(value=owner_id)
                )
            ]
        )
        
        results = []
        offset = None
        batch_size = 100
        
        while True:
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=query_filter,
                limit=batch_size,
                offset=offset
            )
            
            points = scroll_result[0]
            if not points:
                break
            
            for point in points:
                results.append({
                    'content': point.payload['content'],
                    'owner_id': point.payload['owner_id'],
                    'metadata': {k: v for k, v in point.payload.items() if k not in ['content', 'owner_id']}
                })
            
            offset = points[-1].id
        
        return results

    def clear(self):
        self.client.delete_collection(self.collection_name)
        self._ensure_collection()
