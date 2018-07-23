from math import ceil

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


class Material(models.Model):
    title = models.CharField('Название', max_length=300)
    width = models.IntegerField('Ширина', default=0)
    height = models.IntegerField('Высота', default=0)
    depth = models.DecimalField('Толщина', decimal_places=1, max_digits=15, default=0)
    cost = models.DecimalField('Стоимость', decimal_places=2, max_digits=15)
    uid = models.CharField('UID', max_length=100)

    class Meta:
        ordering = ('title',)

    def get_size_string(self):
        return '{}X{}X{}'.format(self.width, self.height, self.depth if self.depth % 1 != 0 else int(self.depth))

    def __unicode__(self):
        return self.title


class Edge(models.Model):
    title = models.CharField('Название', max_length=300)
    cost = models.DecimalField('Стоимость', decimal_places=2, max_digits=15)
    height = models.IntegerField('Высота', default=0)
    depth = models.DecimalField('Толщина', decimal_places=1, max_digits=15, default=0)

    @classmethod
    def get_query_by_material_depth(cls, depth):
        query = Edge.objects.all()
        if depth == 8:
            query = query.filter(height=19, depth=0.4)
        elif 10 <= depth <= 16:
            query = query.filter(height=19, depth__in=[0.4, 0.8, 2])
        elif depth == 25:
            query = query.filter(height=28, depth__in=[0.8, 2])
        return query

    def __unicode__(self):
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    STATUSES = [
        (0, 'Заявка'),
        (1, 'Подтвержден'),
        (2, 'Выполняется'),
        (3, 'Выполнен'),
        (4, 'Выдан'),
    ]
    status = models.IntegerField('Статус', choices=STATUSES, default=0)
    info = models.CharField('Информация о заказе', max_length=1000)
    calculation = models.ForeignKey('Calculation', on_delete=models.SET_NULL, verbose_name='Калькуляция', null=True)


class MaterialWorkCost(models.Model):
    min_d = models.IntegerField('От')
    max_d = models.IntegerField('До (не включая)')
    cost = models.IntegerField()


class EdgeWorkCost(models.Model):
    height = models.IntegerField('Высота', default=0)
    depth = models.DecimalField('Толщина', decimal_places=1, max_digits=15, default=0)
    cost = models.IntegerField()

    @classmethod
    def get_costs(cls, height):
        return EdgeWorkCost.objects.filter(height=height).order_by('depth').values_list('cost', flat=True)


class Calculation(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    data = models.TextField(default='')

    material = models.ForeignKey('Material', on_delete=models.SET_NULL, verbose_name='Материал', null=True)
    edge = models.ForeignKey('Edge', on_delete=models.SET_NULL, verbose_name='Кромка', null=True)

    celery_task_id = models.CharField(max_length=500, default='')
    ready = models.BooleanField(default=False)

    detail_area = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    plate_area = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    time_raspil = models.CharField(max_length=200, default='')
    detail_count = models.IntegerField(default=0)
    plate_count = models.IntegerField(default=0)
    waste_percentage = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    rez_length = models.DecimalField(max_digits=20, decimal_places=3, default=0)

    kromka_04 = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    kromka_08 = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    kromka_20 = models.DecimalField(max_digits=20, decimal_places=3, default=0)

    page_count = models.IntegerField(default=0)

    work_cost = models.DecimalField('Стоимость работы', decimal_places=2, max_digits=15, default=0)
    edge_length = models.IntegerField(default=0)

    def get_work_cost(self):
        material_depth = self.material.depth
        edge_height = self.edge.height
        try:
            material_work_cost = MaterialWorkCost.objects.get(min_d__gte=material_depth, max_d__lt=material_depth).cost
        except MaterialWorkCost.DoesNotExist:
            material_work_cost = 1
        try:
            edge04_work_cost, edge08_work_cost, edge20_work_cost = EdgeWorkCost.get_costs(edge_height)
        except:
            edge04_work_cost, edge08_work_cost, edge20_work_cost = 1, 1, 1

        return Decimal(self.rez_length) * material_work_cost + Decimal(self.kromka_04) * edge04_work_cost + \
               Decimal(self.kromka_08) * edge08_work_cost + Decimal(self.kromka_20) * edge20_work_cost

    def get_edge_length(self):
        total_l = (Decimal(self.kromka_04) + Decimal(self.kromka_08) + Decimal(self.kromka_20) + 3)
        return 5 * ceil(total_l/5)
