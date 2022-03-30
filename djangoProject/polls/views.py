from django.http import JsonResponse, HttpResponse
from polls.vector_model import VectorModel


def index(request):
    res = VectorModel().search(request.GET.get("search"))
    print(res)
    return JsonResponse(res, safe=False)

def article(request):
    page = request.GET.get("article")
    file = open('/Users/kamillahajrullina/PycharmProjects/itis/Выкачка/страница ' + page + '.txt', 'r')
    lines = file.readlines()
    text = ""
    for line in lines:
        text += line
    print(page)
    return HttpResponse(text)
