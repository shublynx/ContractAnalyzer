import numpy as np
from ..utils.redis_client import redis_client
from redis.commands.search.query import Query

class SemanticCache:
    INDEX = "idx:contract_cache"
    # 0.1 is very strict (near-identical). 
    # 0.2 to 0.25 is usually better for "similar" legal questions.
    THRESHOLD = 0.2  

    @classmethod
    def get_hit(cls, vector):
        """
        Searches Redis for the closest existing question vector.
        Uses K-Nearest Neighbors (KNN) to find the top 1 match.
        """
        # The query string for Redis Stack Vector Search
        # @vector is the field name we defined in init_redis.py
        query_str = f"*=>[KNN 1 @vector $vec as score]"
        
        q = (
            Query(query_str)
            .sort_by("score")
            .return_fields("answer", "score")
            .dialect(2)
        )
        
        try:
            # We must pass the vector as bytes for the Redis search
            results = redis_client.ft(cls.INDEX).search(
                q, {"vec": vector.tobytes()}
            )
            
            if results.docs:
                score = float(results.docs[0].score)
                # In Cosine distance, smaller score = more similar
                if score < cls.THRESHOLD:
                    print(f"--- [CACHE HIT] Score: {score:.4f} ---")
                    return results.docs[0].answer
                    
            return None
        except Exception as e:
            print(f"Redis Search Error: {e}")
            return None

    @classmethod
    def set_hit(cls, question, answer, vector):
        """
        Saves a new Q&A pair to the Redis Vector Index.
        """
        # Create a unique key using a simple hash of the question
        # This prevents duplicate keys for the exact same string
        key = f"cache:{hash(question)}"
        
        mapping = {
            "question": question,
            "answer": answer,
            "vector": vector.tobytes() # Vectors MUST be saved as bytes
        }
        
        try:
            # HSET saves the data as a Redis Hash
            # Because we used IndexType.HASH in init_redis, it gets indexed automatically
            redis_client.hset(key, mapping=mapping)
            print(f"--- [CACHE SAVED] Question indexed in Redis ---")
        except Exception as e:
            print(f"Redis Save Error: {e}")