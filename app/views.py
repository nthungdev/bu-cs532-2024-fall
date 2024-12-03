import importlib
from django.shortcuts import render

from app.models import Executive

module_name = 'app.queries'
queries_module = importlib.import_module(module_name)


def index(request):
    executive = Executive.objects.first()

    query_list = []
    for i in range(1, 16):
        query = None
        description = 'None'
        try:
            query = getattr(queries_module, f'query_{i}')
            descriptions = getattr(queries_module, 'query_descriptions')
            description = descriptions.get(i, 'None')
        except AttributeError:
            print(f"Function query_{i} does not exist in the module {module_name}")
        except Exception as e:
            print(f"An error occurred: {e}")

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

    query = None
    result = None
    try:
        query = getattr(queries_module, f'query_{query_index}')
        result = query()
    except AttributeError:
        print(f"Function query_{query_index} does not exist in the module {module_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

    context = {
        "result": result,
        "query_index": query_index
    }
    return render(request, "app/query.html", context)
