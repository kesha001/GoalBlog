from flask import current_app


def ES_search(client, index: str, to_search: str):
    query = {
        "multi_match" : {
            "query":    to_search, 
        }
    }
    # query = { "query": { "match_all": {} }, "size": 5000, "from": 0 }
    # print(query)
    response = client.search(index=index, query=query)

    return response

def search_in_index(index, query):
    es_client = current_app.es_client
    payload = {
        "multi_match": {
            "query": query,

        }
    }

    response = es_client.search(index=index, query=payload)

    idx = [int(hit['_id']) for hit in response['hits']['hits']]

    return idx


def add_to_index(object, index):
    es_client = current_app.es_client
    if not es_client:
        return None
    
    searchable_fields = getattr(object, "__searchable__", [])

    if not searchable_fields:
        return None

    index_data = {}
    for field in searchable_fields:
        index_data[field] = getattr(object, field)
    

    response = es_client.index(index=index, id=object.id, document = index_data)

    return response

def delete_from_index(object, index):
    es_client = current_app.es_client
    if not es_client:
        return None
    
    response = es_client.delete(index=index, id=object.id)

    return response