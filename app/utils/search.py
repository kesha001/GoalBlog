from elasticsearch import Elasticsearch
from flask import current_app

def get_ES_client():
    client = Elasticsearch(
        hosts=current_app.config['ELASTIC_SEARCH_URI']
    )

    if client.ping():
        return client
    
    return None


def ES_search(client, index: str, to_search: str, fields: list):
    query = {
        "multi_match" : {
            "query":    to_search, 
            "fields": fields 
        }
    }
    print(query)
    response = client.search(index=index, query=query)

    return response
