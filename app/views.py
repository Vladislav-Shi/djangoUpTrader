from django.shortcuts import render

from app.models import BaseMenu


# Create your views here.
def generate_menu(request):
    """Т.к. меню может быть несколько и активное определяется по url, то гет параметры самое то"""
    if request.method == 'GET':
        try:
            selected = int(request.GET.get('selected'))
        except:
            selected = None
        menu_objs = BaseMenu.objects.filter(category__name='Категория_1').order_by('parent_id')
        context = {'selected': selected,
                   'Категория_1': menu_objs}
        return render(request, 'index.html', context=context)
