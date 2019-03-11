import os


from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone, dateparse


from fruitsales.models import Sale
from fruitsales.utils import generate_sales_from_csv
from fruits.models import Fruit


class LoginFruitSaleViewAccessTest(TestCase):
    """ログイン状態で各ページにアクセスできることをテスト"""
    def setUp(self):
        fruit = Fruit.objects.create(name='みかん', price=100)
        Sale.objects.create(fruit=fruit, number=5, amount=500,
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-02-24 12:00:00')))

        # Login
        User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_fruitsale_list_view(self):
        url = reverse('fruitsale_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_fruitsale_create_view(self):
        url = reverse('fruitsale_new')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_fruitsale_update_view(self):
        url = reverse('fruitsale_edit', args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_fruitsale_delete_view(self):
        url = reverse('fruitsale_delete', args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class NoLoginFruitSaleViewAccessTest(TestCase):
    """非ログイン状態で各ページにアクセスできない、
    かつログインページにリダイレクトされることをテスト"""
    def setUp(self):
        fruit = Fruit.objects.create(name='みかん', price=100)
        Sale.objects.create(fruit=fruit, number=5, amount=500,
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-02-24 12:00:00')))

    def test_fruitsale_list_view(self):
        url = reverse('fruitsale_list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_fruitsale_create_view(self):
        url = reverse('fruitsale_new')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_fruitsale_update_view(self):
        url = reverse('fruitsale_edit', args=(1,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_fruitsale_delete_view(self):
        url = reverse('fruitsale_delete', args=(1,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)


class LoginFruitSaleViewPostTest(TestCase):
    """ログイン状態でCreate, Update, Deleteができることをテスト"""
    def setUp(self):
        mikan = Fruit.objects.create(name='みかん', price=100)
        Fruit.objects.create(name='イチゴ', price=500)
        Sale.objects.create(fruit=mikan, number=5, amount=500,
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-02-24 12:00:00')))

        # Login
        User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password') 

    def test_fruitsale_create_view_post(self):
        url = reverse('fruitsale_new')
        response = self.client.post(url, {'fruit': 1, 'number': 10,
                'sold_at': '2019-02-24 12:00:00'})
        self.assertRedirects(response, reverse('fruitsale_list'))
        
        sale = Sale.objects.get(id = 2)
        self.assertEquals(sale.fruit.id, 1)
        self.assertEquals(sale.number, 10)
        self.assertEquals(sale.amount, 1000)
        self.assertEquals(sale.sold_at, timezone.make_aware(
                    dateparse.parse_datetime('2019-02-24 12:00:00')))

    def test_fruitsale_update_view_post(self):
        url = reverse('fruitsale_edit', args=(1,))
        response = self.client.post(url, {'fruit': 2, 'number': 20,
                'sold_at': '2019-02-24 13:00:00'})
        self.assertRedirects(response, reverse('fruitsale_list'))
        
        sale = Sale.objects.get(id = 1)
        self.assertEquals(sale.fruit.id, 2)
        self.assertEquals(sale.number, 20)
        self.assertEquals(sale.amount, 500)
        self.assertEquals(sale.sold_at, timezone.make_aware(
            dateparse.parse_datetime('2019-02-24 13:00:00')))


    def test_fruitsale_delete_view_post(self):
        url = reverse('fruitsale_delete', args=(1,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('fruitsale_list'))

        with self.assertRaises(Sale.DoesNotExist):
            Sale.objects.get(id = 1)


class NoLoginFruitSaleViewPostTest(TestCase):
    """非ログイン状態でCreate, Update, DeleteのPostをはじくかテスト"""
    def setUp(self):
        mikan = Fruit.objects.create(name='みかん', price=100)        
        Fruit.objects.create(name='イチゴ', price=500)
        Sale.objects.create(fruit=mikan, number=5, amount=500,
                            sold_at=timezone.make_aware(dateparse.parse_datetime('2019-02-24 12:00:00')))

    def test_fruitsale_create_view_post(self):
        url = reverse('fruitsale_new')
        response = self.client.post(url, {'fruit': 1, 'number': 10,
                'sold_at': '2019-02-24 12:00:00'})
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        
        self.assertEquals(len(Sale.objects.all()), 1)

    def test_fruitsale_update_view_post(self):
        url = reverse('fruitsale_edit', args=(1,))
        response = self.client.post(url, {'fruit': 2, 'number': 20,
                'sold_at': '2019-02-24 13:00:00'})
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        
        sale = Sale.objects.get(id = 1)
        self.assertEquals(sale.fruit.id, 1)
        self.assertEquals(sale.number, 5)
        self.assertEquals(sale.amount, 500)
        self.assertEquals(sale.sold_at, timezone.make_aware(
                    dateparse.parse_datetime('2019-02-24 12:00:00')))

    def test_fruit_delete_view_post(self):
        url = reverse('fruitsale_delete', args=(1,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

        sale = Sale.objects.get(id = 1)
        self.assertEquals(sale.fruit.id, 1)
        self.assertEquals(sale.number, 5)
        self.assertEquals(sale.amount, 500)
        self.assertEquals(sale.sold_at, timezone.make_aware(
                    dateparse.parse_datetime('2019-02-24 12:00:00')))

class CsvInputTest(TestCase):
    """CSV入力によるレコード登録機能のテスト"""
    def setUp(self):
        Fruit.objects.create(name='ブルーベリー',price=100)
        Fruit.objects.create(name='りんご',price=200)

    def test_correct_csv(self):
        """正しいフォーマットの場合、ファイル内と同じだけのレコードが登録されることをテスト"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/correct_records.csv'
                    ),
                    mode='rb'
                )

        sales = generate_sales_from_csv(file)

        self.assertEqual(len(sales), 2)

        sale1 = Sale.objects.get(id=1)
        self.assertEquals(sale1.fruit.id, 1)
        self.assertEquals(sale1.number, 3)
        self.assertEquals(sale1.amount, 900)
        self.assertEquals(sale1.sold_at, timezone.make_aware(
            dateparse.parse_datetime('2016-02-02 10:30')))

        sale2 = Sale.objects.get(id=2)
        self.assertEquals(sale2.fruit.id, 2)
        self.assertEquals(sale2.number, 3)
        self.assertEquals(sale2.amount, 270)
        self.assertEquals(sale2.sold_at, timezone.make_aware(
            dateparse.parse_datetime('2016-02-01 10:35')))

    def test_invalid_csv_1(self):
        """日付フォーマットがおかしい場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records1.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = generate_sales_from_csv(file)
    
    def test_invalid_csv_2(self):
        """果物マスタに存在しない果物名を指定した場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records2.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = generate_sales_from_csv(file)

    def test_invalid_csv_3(self):
        """個数指定が負の場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records3.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = generate_sales_from_csv(file)

    def test_invalid_csv_4(self):
        """カンマ区切りの要素数が4でない場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records4.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = generate_sales_from_csv(file)

    def test_invalid_csv_5(self):
        """二つ目からのレコードのフォーマットがおかしい場合、一つ目のレコードは保存されない"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records5.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = generate_sales_from_csv(file)

        self.assertEqual(len(Sale.objects.all()), 0)