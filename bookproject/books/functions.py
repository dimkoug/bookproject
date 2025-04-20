from django.http import JsonResponse
from django.db.models import Q
from core.functions import get_sb_data
from books.models import Category,Author


def get_sb_categories_data(request):
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    model = Category
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        if request.user.is_superuser:
            data = model.objects.filter(q_objects)
        else:
            data = model.objects.select_related('profile').filter(q_objects,profile=request.user.profile)
    else:
        if request.user.is_superuser:
            data = model.objects.all()
        else:
            data = model.objects.sellect_related('profile').filter(profile=request.user.profile)
    
    
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)


def get_sb_authors_data(request):
    results = []
    if not request.user.is_authenticated:
        return JsonResponse(results, safe=False)
    model = Author
    q_objects = Q()
    d_objects = []
    search = request.GET.get('search')
    if search and search != '':
        for f in  model._meta.get_fields():
            if f.__class__.__name__  in ['CharField', 'TextField']:
                str_q = f"Q({f.name}__icontains=str('{search}'))"
                q_obj = eval(str_q)
                q_objects |= q_obj
        if request.user.is_superuser:
            data = model.objects.filter(q_objects)
        else:
            data = model.objects.select_related('profile').filter(q_objects,profile=request.user.profile)
    else:
        if request.user.is_superuser:
            data = model.objects.all()
        else:
            data = model.objects.sellect_related('profile').filter(profile=request.user.profile)
    
    
    for d in data:
        d_objects.append({
            "id": d.pk,
            "text": d.__str__()
        })
    return JsonResponse({"results": d_objects}, safe=False)