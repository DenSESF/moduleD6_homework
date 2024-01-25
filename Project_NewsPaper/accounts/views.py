# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse

from whiteboard.models import Category


@login_required
def join_authors(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('news:news')


@login_required
def subscribe_category(request):
    user = request.user
    url = reverse('news:news')
    if request.POST.get('cat') is not None:
        cat_id = request.POST.get("cat")
        category = Category.objects.get(pk=cat_id)
        if not category.subscribers.filter(username=user).exists():
            category.subscribers.add(user)
        url += f'?cat={cat_id}'
    return redirect(url)
