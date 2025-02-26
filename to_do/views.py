# from django.shortcuts import render
# from .models import Task

# def task_list(request):
#     tasks = Task.objects.all()
#     return render(request, 'to_do/index.html', {'tasks': tasks})


from django.shortcuts import render
from django.http import HttpResponse

def task_list(request):
    
    return render(request, 'to_do/index.html')
