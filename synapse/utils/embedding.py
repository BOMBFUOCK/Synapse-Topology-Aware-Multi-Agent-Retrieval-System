import yaml
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingModel:
    _instance = None
    _model = None

    @classmethod
    def get_model(cls, model_name: str = None):
        if cls._instance is None:
            cls._instance = cls()
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            model_name = model_name or config['embedding']['model_name']
            cls._model = SentenceTransformer(model_name)
        return cls._model


def get_embedding(text: str) -> List[float]:
    model = EmbeddingModel.get_model()
    embedding = model.encode(text)
    return embedding.tolist()


def get_embeddings(texts: List[str]) -> List[List[float]]:
    model = EmbeddingModel.get_model()
    embeddings = model.encode(texts)
    return embeddings.tolist()
