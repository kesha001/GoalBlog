from flask import current_app


def search_in_index(index, query, per_page, starting_num):
    es_client = current_app.es_client
    if not es_client:
        return [], 0
    payload = {
        "multi_match": {
            "query": query,
        }
    }

    response = es_client.search(index=index, query=payload, 
                                size=per_page, from_=starting_num)

    idx = [int(hit['_id']) for hit in response['hits']['hits']]
    total_hits = response['hits']['total']['value']

    # print(response)

    return idx, total_hits


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