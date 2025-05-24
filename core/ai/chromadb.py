from chromadb import HttpClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
from chromadb.utils.data_loaders import ImageLoader

chroma = HttpClient(host="localhost", port=8010)

openai_ef = OpenAIEmbeddingFunction(
    model_name="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY"),
)

data_loader = ImageLoader()
