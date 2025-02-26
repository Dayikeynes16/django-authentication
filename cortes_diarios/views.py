from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def DS(request):
    return render(request, 'cortes/index.html')