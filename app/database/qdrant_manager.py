import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient


load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")


if not QDRANT_URL:
    raise ValueError("QDRANT_URL is not set in the .env file")

if not QDRANT_API_KEY:
    raise ValueError("QDRANT_API_KEY is not set in the .env file")


client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)


if __name__ == "__main__":

    try:
        collections = client.get_collections()

        print("✅ Qdrant connection successful!")
        print("Available collections:")

        for collection in collections.collections:
            print(f"- {collection.name}")

    except Exception as e:
        print("❌ Qdrant connection failed!")
        print(e)