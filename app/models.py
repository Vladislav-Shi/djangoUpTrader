from django.db import models


class CategoryMenu(models.Model):
    """Категория каталогов
    Нужна чтобы ограничить выборку без доп запросов в бд"""
    name = models.CharField(max_length=64, unique=True)


# Create your models here.
class BaseMenu(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название', unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    category = models.ForeignKey('CategoryMenu', null=True, on_delete=models.SET_NULL)

    @property
    def level(self):
        """Уровень вложения меню"""
        return self.parent is not None and self.parent.level + 1 or 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Меню'
