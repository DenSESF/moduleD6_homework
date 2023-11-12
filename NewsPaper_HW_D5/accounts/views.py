# from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect


@login_required
def join_authors(request):
   user = request.user
   authors_group = Group.objects.get(name='authors')
   if not request.user.groups.filter(name='authors').exists():
       authors_group.user_set.add(user)
   return redirect('/news/')
