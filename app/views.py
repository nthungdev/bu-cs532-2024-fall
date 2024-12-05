from django.shortcuts import render

# from app.models import Executive
import app.utils as utils


def index(request):
    query_list = []
    for i in range(1, 16):
        query = utils.get_query_fn(i)
        description = utils.get_query_description(i)

        def query_fn():
            def wrapped():
                index = i
                print(f'execute query {index}')
                if query:
                    query()
            return wrapped

        query_item = {
            'name': f'query {i}',
            'description': description,
            'query_fn': query_fn,
        }
        query_list.append(query_item)

    print(query_list)
    context = {
        'query_list': query_list,
    }
    return render(request, "app/index.html", context)


def query(request, query_index):
    print(f'query {query_index}')

    query = utils.get_query_fn(query_index)
    description = utils.get_query_description(query_index)
    result = None
    json_query = utils.get_query(query_index)
    print(" query : ", json_query)
    try:
        result = query()
    except AttributeError as e:
        print(e)
        print(f"Function query_{query_index} does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")

    context = {
        "json_query": json_query,
        "result": result,
        "query_index": query_index,
        "description": description,
    }
    return render(request, "app/query.html", context)
