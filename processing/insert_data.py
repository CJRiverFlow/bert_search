import pandas as pd
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
sentence_transformer = SentenceTransformer("distiluse-base-multilingual-cased-v1")
es_client = Elasticsearch("localhost:9200")
INDEX_NAME = "bert_betmaster"

def index_qa_pairs(data): 
    for text in data:
        embedding = sentence_transformer.encode(text).tolist()
        data = {
            "text": text,
            "embedding": embedding,
        }

        es_client.index(
                index=INDEX_NAME,
                body=data
            )


def get_sentences(file_path):
    file = pd.read_csv(file_path)
    text_column = file['Text']
    return text_column

text_list = get_sentences('./files/Betmaster.csv')
index_qa_pairs(text_list)
print("Completado")