from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone, dateparse


class Sale(models.Model):
    """販売情報モデル"""
    fruit = models.ForeignKey('fruits.Fruit', null=True, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(null=True)
    amount = models.PositiveIntegerField(null=True)
    sold_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.fruit.name

    def get_absolute_url(self):
        return reverse('fruitsale_list')


def generate_sales_from_csv(file):
    import csv
    import io
    from fruits.models import Fruit

    records_csv = io.TextIOWrapper(file, encoding='utf-8')

    # 全ての行を反復
    records = csv.reader(records_csv, delimiter=',')
    sale_list = []
    for row in records:
        if len(row) != 4:
            raise ValidationError('要素数が４以外です: ' + ','.join(row))

        # Fruitオブジェクトを取得
        fruit = Fruit.objects.filter(name=row[0])

        if not fruit:
            raise ValidationError('果物マスタにない果物名が指定されました: {}'.format(row[0]))

        # 販売日時をパース
        try:
            sold_at = dateparse.parse_datetime(row[3])
        except ValueError:
            raise ValidationError('不正な日時指定です: {}'.format(row[3]))
            
        if sold_at is None:
            raise ValidationError('不正な日時フォーマットです: {}'.format(row[3]))

        # ローカルタイム化
        sold_at = timezone.make_aware(sold_at)

        # 複数候補がある場合はインデックス０のものを使用
        sale = Sale(fruit=fruit[0], number=row[1], amount=row[2], sold_at=sold_at)

        sale_list.append(sale)

    # 保存
    for sale in sale_list:
        sale.save()

    # 新規作成したオブジェクトのQuerysetを返す
    return Sale.objects.filter(id__in=[sale.id for sale in sale_list])