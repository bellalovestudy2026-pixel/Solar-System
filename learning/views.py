from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('learning:home')
    form = UserCreationForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('learning:login')
    return render(request, 'learning/signup.html', {'form': form})


def home(request):
    return render(request, 'learning/home.html')


def science(request):
    return render(request, 'learning/science.html')

def solar_system(request):
    return render(request, 'learning/solar_system.html')
