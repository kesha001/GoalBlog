from flask import current_app


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

def add_to_index(object, index):
    es_client = current_app.es_client
    if not es_client:
        return None
    
    index_data = {}

    for field in  getattr(object, "__searchable__"):
        index_data[field] = getattr(object, field)
    
    print(index_data, index)

    response = es_client.index(index=index, id=object.id, document = index_data)

    return response

def delete_from_index(object, index):
    es_client = current_app.es_client
    if not es_client:
        return None
    
    response = es_client.delete(index=index, id=object.id)

    return response