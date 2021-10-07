import argparse
from elasticsearch import Elasticsearch

es_client = Elasticsearch("localhost:9200")
EMBEDDING_DIMS = 512
# INDEX_NAME = "bert_betmaster"

def create_index(INDEX_NAME):
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--index_name', type= str, required=True)
    args = parser.parse_args()
    create_index(args.index_name)
    print("Indexes created")