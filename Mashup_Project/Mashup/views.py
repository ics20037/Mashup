from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'mashup\index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'mashup/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'mashup/profile.html')
