from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

from lists.forms import ExistingListItemForm, ItemForm, NewListForm
from lists.models import List

User = get_user_model()


def home_page(request):
    return render(request, "home.html", {"form": ItemForm()})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        list_ = form.save(owner=request.user)
        return redirect(list_)
    return render(request, "home.html", {"form": form})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(
        request,
        "list.html",
        {"list": list_, "form": form},
    )


def my_lists(request, email):
    owner = User.objects.get(email=email)
    shared_with = List.objects.filter(shared_with=owner).all()
    return render(request, "my_lists.html", {"owner": owner, "shared_lists": shared_with})


def share_my_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        email = request.POST["sharee"]
        list_.shared_with.add(email)

    return redirect(list_.get_absolute_url())
