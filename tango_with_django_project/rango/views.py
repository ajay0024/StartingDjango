from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Category, Page
from .forms import CategoryForm, PageForm


def index(request):
    category_list = Category.objects.order_by("-likes")[:5]
    pages_list = Page.objects.order_by("-views")[:5]
    context_dict = {"categories": category_list, "pages": pages_list}
    return render(request, 'rango/index.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category)
    context_dict["pages"] = pages
    context_dict["category"] = category
    # try:
    #     category = Category.objects.get(slug=category_name_slug)
    #     pages = Page.objects.filter(category=category)
    #     context_dict["pages"] = pages
    #     context_dict["category"] = category
    # except Category.DoesNotExist:
    #     context_dict["pages"] = None
    #     context_dict["category"] = None
    return render(request, 'rango/category.html', context_dict)


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            print("Valid Form")
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {"form": form})


def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                print("Valid Form")
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict={"form":form, "category":category}
    return render(request, 'rango/add_page.html', context_dict)


def about(request):
    context_dict = {}
    print(request.method)
    print(request.user)
    return render(request, 'rango/about.html', context=context_dict)