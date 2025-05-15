import os
from dotenv import load_dotenv
import pinecone

load_dotenv()
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)
index_name = os.getenv("PINECONE_INDEX_NAME")


# 如果不存在則建立
if index_name not in pinecone.list_indexes():
    pinecone.create_index(name=index_name, dimension=1536, metric="cosine")

index = pinecone.Index(index_name)

def upsert_faq(faq_id, embedding, metadata):
    index.upsert(vectors=[(faq_id, embedding, metadata)])

def query_faq(user_embedding, top_k=3):
    query_vector = user_embedding  # 明確命名
    result = index.query(vector=query_vector, top_k=3)
    return result['matches']

def delete_faq(faq_id):
    index.delete(ids=[faq_id])
