from django.shortcuts import render, redirect
from .forms import UserModelForm
from .models import User, Department

# Create your views here.


def user_list(request):
    """
    the list of the client
    :return:
    """
    data_list = User.objects.all()

    return render(request, 'user_list.html', {'data_list': data_list})


def user_create(request):
    """
    Create a client
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_update.html', {'form': form})
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')

        User.objects.create_user(username=username, password=password, email=email)
        return redirect('/user/list/')
    return render(request, 'user_update.html', {'form': form})


def department_list(request):
    """
    the list of the department
    :return:
    """
    data_list = Department.objects.all()

    return render(request, 'department_list.html', {'data_list': data_list})
