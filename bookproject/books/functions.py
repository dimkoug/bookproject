from django.http import JsonResponse
from django.db.models import Q
from core.functions import get_sb_data
from books.models import Category,Author


def get_sb_categories_data(request):
    if request.user.is_anonymous:
        return JsonResponse({"results":[]},safe=False)
    queryset = Category.objects.filter(profile_id=request.user.profile)
    q_objects = Q()
    q = request.GET.get('search')
    for f in  Category._meta.get_fields():
        if f.__class__.__name__  in ['CharField', 'TextField']:
            str_q = f"Q({f.name}__icontains=str('{q}'))"
            q_obj = eval(str_q)
            q_objects |= q_obj
    return get_sb_data(queryset,q_objects)


def get_sb_authors_data(request):
    if request.user.is_anonymous:
        return JsonResponse({"results":[]},safe=False)
    queryset = Author.objects.filter(profile_id=request.user.profile)
    q_objects = Q()
    q = request.GET.get('search')
    for f in  Author._meta.get_fields():
        if f.__class__.__name__  in ['CharField', 'TextField']:
            str_q = f"Q({f.name}__icontains=str('{q}'))"
            q_obj = eval(str_q)
            q_objects |= q_obj
    return get_sb_data(queryset,q_objects)