import numpy as np
from django.core.management.base import BaseCommand
from contracts.utils.redis_client import redis_client
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.index_definition import IndexDefinition, IndexType

class Command(BaseCommand):
    help = "Initializes the Redis Vector Search Index (HASH-based)"

    def handle(self, *args, **options):
        index_name = "idx:contract_cache"
        
        try:
            # Check if index already exists
            redis_client.ft(index_name).info()
            self.stdout.write(self.style.SUCCESS(f"Index '{index_name}' already exists."))
        except:
            self.stdout.write(f"Creating index '{index_name}'...")
            
            # Define the Schema (768-dim for Gemini/All-MiniLM)
            schema = (
                TextField("$.question", as_name="question"),
                TextField("answer", as_name="answer"),
                VectorField("vector", "HNSW", {
                    "TYPE": "FLOAT32",
                    "DIM": 768,
                    "DISTANCE_METRIC": "COSINE",
                }, as_name="vector"),
            )
            
            # Create the Index as HASH (matches your hset in cache.py)
            redis_client.ft(index_name).create_index(
                fields=schema,
                definition=IndexDefinition(prefix=["cache:"], index_type=IndexType.HASH)
            )
            self.stdout.write(self.style.SUCCESS("Successfully initialized Vector Index."))