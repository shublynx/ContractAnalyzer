import numpy as np
import hashlib
import os
from ..utils.redis_client import redis_client
from redis.commands.search.query import Query

class SemanticCache:
    INDEX = "idx:contract_cache"
    THRESHOLD = 0.2  

    def __init__(self):
        self.client = redis_client

    @classmethod
    def get_hit(cls, vector):
        query_str = f"*=>[KNN 1 @vector $vec as score]"
        q = (
            Query(query_str)
            .sort_by("score")
            .return_fields("answer", "score")
            .dialect(2)
        )
        
        try:
            results = redis_client.ft(cls.INDEX).search(
                q, {"vec": vector.tobytes()}
            )
            
            if results.docs:
                doc = results.docs[0]
                score = float(doc.score)
                
                if score < cls.THRESHOLD:
                    print(f"--- [CACHE HIT] Score: {score:.4f} ---")
                    # Try both attribute and dictionary access
                    answer = getattr(doc, 'answer', None)
                    if not answer and hasattr(doc, '__dict__'):
                        answer = doc.__dict__.get('answer')
                    return answer
            return None
        except Exception as e:
            print(f"Redis Search Error: {e}")
            return None

    @classmethod
    def set_hit(cls, question, answer, vector):
        question_hash = hashlib.md5(question.encode()).hexdigest()
        key = f"cache:{question_hash}"
        
        mapping = {
            "question": question,
            "answer": answer,
            "vector": vector.tobytes()
        }
        
        try:
            redis_client.hset(key, mapping=mapping)
            print(f"--- [CACHE SAVED] Question indexed in Redis ---")
        except Exception as e:
            print(f"Redis Save Error: {e}")