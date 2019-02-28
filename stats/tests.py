from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone, dateparse


from fruits.models import Fruit
from fruitsales.models import Sale
from stats.utils import get_sales_filtered_sold_at, cumulate_sales_fruitwise


class LoginStatsViewAccessTest(TestCase):
    """ログイン状態でページにアクセスできることをテスト"""
    def setUp(self):
        User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password') 

    def test_stats_view(self):
        url = reverse('fruitsale_stats')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class NoLoginStatsViewAccessTest(TestCase):
    """非ログイン状態でページにアクセスできない、
    かつログインページにリダイレクトされることをテスト"""
    def setUp(self):
        pass

    def test_stats_view(self):
        url = reverse('fruitsale_stats')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)


class GetSalesFilteredSoldAtTest(TestCase):
    """get_sales_filtered_sold_at関数のテスト"""
    def setUp(self):
        f1 = Fruit.objects.create(name='リンゴ', price=300)
        f2 = Fruit.objects.create(name='オレンジ', price=200)

        # Sale objects
        Sale.objects.create(fruit=f1, number=5, amount=1500, 
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-03-01 00:00:00')))
        Sale.objects.create(fruit=f2, number=10, amount=3000, 
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-02-28 23:59:59')))

    def test_get_sales_filtered_sold_at_1(self):
        """正しいレコードが取得されることをテスト"""
        start = timezone.make_aware(dateparse.parse_datetime('2019-03-01 00:00:00'))
        end = timezone.make_aware(dateparse.parse_datetime('2019-03-01 00:00:01'))

        sales = get_sales_filtered_sold_at(start, end)

        self.assertEquals(len(sales), 1)
        self.assertEquals(sales[0].fruit.name, 'リンゴ')
        self.assertEquals(sales[0].number, 5)
        self.assertEquals(sales[0].amount, 1500)
    
    def test_get_sales_filtered_sold_at_2(self):
        """正しいレコードが取得されることをテスト"""
        start = timezone.make_aware(dateparse.parse_datetime('2019-02-28 23:59:59'))
        end = timezone.make_aware(dateparse.parse_datetime('2019-03-01 00:00:01'))

        sales = get_sales_filtered_sold_at(start, end)

        self.assertEquals(len(sales), 2)
        self.assertEquals(sales[0].fruit.name, 'リンゴ')
        self.assertEquals(sales[0].number, 5)
        self.assertEquals(sales[0].amount, 1500)
        self.assertEquals(sales[1].fruit.name, 'オレンジ')
        self.assertEquals(sales[1].number, 10)
        self.assertEquals(sales[1].amount, 3000)


class CumulateSalesFruitwiseTest(TestCase):
    """cumulate_sales_fruitwiseで統計量が正しく計算されるかどうかのテスト"""
    def setUp(self):
        f1 = Fruit.objects.create(name='リンゴ', price=300)
        f2 = Fruit.objects.create(name='オレンジ', price=200)

        # Sale objects
        Sale.objects.create(fruit=f1, number=5, amount=1500, 
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-03-01 00:00:00')))
        Sale.objects.create(fruit=f1, number=10, amount=3000, 
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-02-28 23:59:59')))
        Sale.objects.create(fruit=f1, number=2, amount=600, 
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-03-08 07:30:00')))
        Sale.objects.create(fruit=f2, number=11, amount=2200, 
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-03-15 09:30:00')))
        Sale.objects.create(fruit=f2, number=4, amount=800, 
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-03-22 15:30:00')))


    def test_cumulate_sales_fruitwise_1(self):
        """正しい集計値が計算されることをテスト"""
        start = timezone.make_aware(dateparse.parse_datetime('2019-03-01 00:00:00'))
        end = timezone.make_aware(dateparse.parse_datetime('2019-04-01 00:00:00'))

        sales_amount, details = cumulate_sales_fruitwise(start, end)

        self.assertEquals(sales_amount, 5100)
        self.assertEquals(len(details), 2)

        self.assertEquals(details[0]['name'], 'リンゴ')
        self.assertEquals(details[0]['number'], 7)
        self.assertEquals(details[0]['amount'], 2100)

        self.assertEquals(details[1]['name'], 'オレンジ')
        self.assertEquals(details[1]['number'], 15)
        self.assertEquals(details[1]['amount'], 3000)

    def test_cumulate_sales_fruitwise_2(self):
        """正しい集計値が計算されることをテスト"""
        start = timezone.make_aware(dateparse.parse_datetime('2019-02-28 23:59:59'))
        end = timezone.make_aware(dateparse.parse_datetime('2019-04-01 00:00:00'))

        sales_amount, details = cumulate_sales_fruitwise(start, end)

        self.assertEquals(sales_amount, 8100)
        self.assertEquals(len(details), 2)

        self.assertEquals(details[0]['name'], 'リンゴ')
        self.assertEquals(details[0]['number'], 17)
        self.assertEquals(details[0]['amount'], 5100)

        self.assertEquals(details[1]['name'], 'オレンジ')
        self.assertEquals(details[1]['number'], 15)
        self.assertEquals(details[1]['amount'], 3000)