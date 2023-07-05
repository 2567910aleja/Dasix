from django.shortcuts import render
def categoria_list(request):
    data={

    }
    return render(request,'categoria/list.html',data)