import pandas as pd
import argparse
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
sentence_transformer = SentenceTransformer("distiluse-base-multilingual-cased-v1")
es_client = Elasticsearch("localhost:9200")
# INDEX_NAME = "bert_betmaster"

def index_pairs(data, INDEX_NAME): 
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--index_name', type= str, required=True)
    parser.add_argument('--file_path', type= str, required=True)
    args = parser.parse_args()
 
    text_list = get_sentences(args.file_path)
    index_pairs(text_list, args.index_name)
    print("Completado")