from django.shortcuts import render
from item.models import Category, Item

from .forms import SignUpForm

# Create your views here.
def index(request):
    Items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    return render(request, 'core/index.html', {
        'Items': Items,
        'categories': categories,
    })

def contact(request):
    return render(request, 'core/contact.html')
def signup(request):
        form = SignUpForm()

        return render(request, 'core/signup.html', {
            'form': form,
        })