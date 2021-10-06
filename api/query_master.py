from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch

class QueryMaster:
    def __init__(self):
        self.ENCODER_BOOST = 10
        self.sentence_transformer = SentenceTransformer("distiluse-base-multilingual-cased-v1")
        self.es_client = Elasticsearch("localhost:9200")

    def query_question(self, index_name, query: str, top_n: int=1):
        embedding = self.sentence_transformer.encode(query).tolist()
        es_result = self.es_client.search(
            index=index_name,
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
                                "encoder_boost": self.ENCODER_BOOST,
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
        return clean_result