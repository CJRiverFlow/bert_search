from elasticsearch import Elasticsearch

es_client = Elasticsearch("localhost:9200")

INDEX_NAME = "bert_betmaster"

EMBEDDING_DIMS = 512

def create_index() -> None:

    es_client.indices.delete(index=INDEX_NAME, ignore=404)

    es_client.indices.create(
        index=INDEX_NAME,
        ignore=400,
        body={
            "mappings": {
                "properties": {
                    "embedding": {
                        "type": "dense_vector",
                        "dims": EMBEDDING_DIMS,
                    },
                    "text": {
                        "type": "text",
                    }
                }
            }
        }
    )

create_index()
print("Indexes created")