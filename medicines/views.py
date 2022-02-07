from django.shortcuts import render

# Create your views here.


# home page
def index_page(request):
    return render(request, 'index.html')