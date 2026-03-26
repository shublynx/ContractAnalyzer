import numpy as np
from contracts.utils.redis_client import redis_client
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.index_definition import IndexDefinition, IndexType

def initialize_redis_index():
    INDEX_NAME = "idx:contract_cache"
    
    try:
        # Check if index already exists
        redis_client.ft(INDEX_NAME).info()
        print("Index already exists!")
    except:
        # Define the schema
        schema = (
            TextField("question"), # The original text for debugging
            TextField("answer"),   # The Gemini answer we want to return
            VectorField(
                "vector", 
                "HNSW", { # HNSW is the standard algorithm for fast vector search
                    "TYPE": "FLOAT32", 
                    "DIM": 768, 
                    "DISTANCE_METRIC": "COSINE"
                }
            )
        )
        
        # Create the index
        redis_client.ft(INDEX_NAME).create_index(
            fields=schema,
            definition=IndexDefinition(prefix=["cache:"], index_type=IndexType.HASH)
        )
        print("Successfully created Redis Vector Index!")

if __name__ == "__main__":
    initialize_redis_index()