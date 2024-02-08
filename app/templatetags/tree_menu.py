from typing import Optional

from django import template
from django.db.models import QuerySet

from app.models import BaseMenu

register = template.Library()


def _add_child(id, parents_dict: dict, result_dict: dict, deep: int = 0, obj_id: Optional[int] = None):
    """
    :param id: id текущего пункта меню
    :param parents_dict: словарь, где ключи родитель, значения список наследников.
    :param result_dict: словарь, где ключи id записи, значение её остальные поля
    :param deep: глубина вложенности меню
    :param obj_id: id "выбранного" обьекта, нужно т.к. по ТЗ что под этим пунктом развернуто
    :return: список подходящий для отрисовки
    """
    result = result_dict[id]
    if id == obj_id:
        deep += 1
    if deep <= 0:
        return result
    if id in parents_dict:
        result['children'] = []
        for i in parents_dict[id]:
            result['children'].append(_add_child(i, parents_dict, result_dict, deep - 1, obj_id))
    return result


def deep_level(result_dict: dict, obj_id: int):
    """Функция чтобы узнать глубину вложенности чтобы корреттно все обрезать"""
    parent_id = result_dict[obj_id]['parent_id']
    return parent_id is not None and deep_level(result_dict, parent_id) + 1 or 0


def make_dict_with_child(menu_objs: QuerySet, id_obj: Optional[int]):
    """Функция строит древовидное меню. Так как по ТЗ необходимо все делать в 1 запрос,
    то сначала все выбираем по категории, а потом 'обрезаем' лишнее"""
    result_dict = {item['id']: item for item in menu_objs.values()}
    if id_obj not in result_dict:
        return [item for item in result_dict.values() if item['parent_id'] is None]
    # Узнаем глубину вложенности
    deep = deep_level(result_dict, id_obj)
    # Словарь отсортированный по родителям
    # Нужен чтобы пройтись всего раз
    parents_dict = {}
    for id, values in result_dict.items():
        if values['parent_id'] in parents_dict:
            parents_dict[values['parent_id']].append(id)
        else:
            parents_dict[values['parent_id']] = []
            parents_dict[values['parent_id']].append(id)

    # Добавляем
    result = [_add_child(id, parents_dict, result_dict, deep, id_obj) for id in parents_dict[None]]
    return result


@register.inclusion_tag("tree_menu.html", takes_context=True)
def draw_menu(context: dict, menu_name: str):
    """запрос к бд идет из вызываемой вьюхи
    @:param menu_name: Название менюшки это также ключ в context с обьектами"""
    if context['selected'] is None:
        menu = context[menu_name].filter(parent=None).values()
    else:
        menu = make_dict_with_child(context[menu_name], context['selected'])
    return {
        'options': menu
    }
