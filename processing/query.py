from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
sentence_transformer = SentenceTransformer("distiluse-base-multilingual-cased-v1")
es_client = Elasticsearch("localhost:9200")
INDEX_NAME = "bert_betmaster"

ENCODER_BOOST = 10

def query_question(query: str, top_n: int=3):
    embedding = sentence_transformer.encode(query).tolist()
    es_result = es_client.search(
        index=INDEX_NAME,
        body={
            "from": 0,
            "size": top_n,
            "_source": ["text"],
            "query": {
                "script_score": {
                    "query": {
                        "match": {
                            "text": query
                        }
                    },
                    "script": {
                        "source": """
                            (cosineSimilarity(params.query_vector, doc["embedding"]) + 1)
                        """,
                        "params": {
                            "query_vector": embedding,
                            "encoder_boost": ENCODER_BOOST,
                        },
                    },
                }
            }
        }
    )
    hits = es_result["hits"]["hits"]
    clean_result = []
    for item in hits:
        clean_result.append({
            "text": item["_source"]["text"],
            "score": item["_score"],
        })
    print(clean_result)
    return clean_result

query_question("¿Cuales son los requer", 3)