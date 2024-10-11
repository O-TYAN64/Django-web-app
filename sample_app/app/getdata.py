from django.http import HttpResponse

def write_csv(data):
    name = session_storage.get('name')
    print(f"{name}")
    return HttpResponse("Hello, world!")
