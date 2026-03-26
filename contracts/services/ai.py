import google.generativeai as genai
from django.conf import settings


class AIService:
    def __init__(self):
        # We store the configuration state here
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = "models/gemini-embedding-001"

    def generate_embeddings(self, text_list):
        result = genai.embed_content(
            model=self.model_name,
            content=text_list,
            task_type="retrieval_document",
            output_dimensionality=768
        )
        return result['embedding']