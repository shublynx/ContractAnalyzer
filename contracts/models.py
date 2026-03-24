import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import transaction

from .utils import extract_text_from_pdf, get_text_chunks, generate_gemini_embeddings

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email' # Log in with email
    REQUIRED_FIELDS = ['username'] # Username still required by Django internally


class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contracts')
    file = models.FileField(upload_to='contracts/%Y/%m/%d/')
    name = models.CharField(max_length=255)
    raw_text = models.TextField(blank=True, null=True) # Where the extracted PDF text lives
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Only extract text if it's a new file or hasn't been extracted yet
        if self.file and not self.raw_text:
            self.raw_text = extract_text_from_pdf(self.file)
        super().save(*args, **kwargs)

        # Generate chunks if it don't exist
        if self.raw_text and not self.chunks.exists():
            # Wrap in a transaction for safety
            with transaction.atomic():
                # A. Slice the text
                text_list = get_text_chunks(self.raw_text)
                
                # B. Generate Vectors (The Gemini API Call)
                # Note: Gemini allows up to 100 texts per batch
                vectors = generate_gemini_embeddings(text_list)
                
                # C. Prepare the Objects
                chunk_objects = [
                    ContractChunk(
                        contract=self,
                        content=text_list[i],
                        embedding=vectors[i],
                        chunk_index=i
                    ) for i in range(len(text_list))
                ]
                
                # D. High-Performance Bulk Insert
                ContractChunk.objects.bulk_create(chunk_objects)

    def __str__(self):
        return f"{self.name} - {self.user.email}"
    

from pgvector.django import VectorField

class ContractChunk(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField() # The actual text snippet
    
    # dimensions=1536 is the standard for OpenAI (text-embedding-3-small)
    # If you use a different model later, we can adjust this. 
    # 768 Gemini for now 
    embedding = VectorField(dimensions=768, null=True, blank=True)
    
    chunk_index = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This helps with retrieval speed later
        indexes = [
            models.Index(fields=['contract', 'chunk_index']),
        ]

    def __str__(self):
        return f"{self.contract.name} - Chunk {self.chunk_index}"