from pgvector.django import CosineDistance
from ..models import ContractChunk

def get_similar_chunks(contract_id, query_vector, limit=5):
    """Filters by ID and sorts by distance. Pure database logic."""
    return ContractChunk.objects.filter(
        contract_id=contract_id
    ).annotate(
        distance=CosineDistance('embedding', query_vector)
    ).order_by('distance')[:limit]