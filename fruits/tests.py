from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


from .models import Fruit


class LoginFruitViewAccessTest(TestCase):
    """ログイン状態で各ページにアクセスできることをテスト"""
    def setUp(self):
        Fruit.objects.create(name='みかん', price=100)
        User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password') 

    def test_fruit_list_view(self):
        url = reverse('fruit_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_fruit_create_view(self):
        url = reverse('fruit_new', args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_fruit_update_view(self):
        url = reverse('fruit_edit', args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_fruit_delete_view(self):
        url = reverse('fruit_delete', args=(1,))
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


class NoLoginFruitViewAccessTest(TestCase):
    """非ログイン状態で各ページにアクセスできない、
    かつログインページにリダイレクトされることをテスト"""
    def setUp(self):
        Fruit.objects.create(name='みかん', price=100)
        User.objects.create_user(username='testuser', password='password')

    def test_fruit_list_view(self):
        url = reverse('fruit_list')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_fruit_create_view(self):
        url = reverse('fruit_new')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_fruit_update_view(self):
        url = reverse('fruit_edit', args=(1,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_fruit_delete_view(self):
        url = reverse('fruit_delete', args=(1,))
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)


class LoginFruitViewPostTest(TestCase):
    """ログイン状態でCreate, Update, Deleteができることをテスト"""
    def setUp(self):
        Fruit.objects.create(name='みかん', price=100)
        User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password') 

    def test_fruit_create_view_post(self):
        url = reverse('fruit_new')
        response = self.client.post(url, {'name': 'リンゴ', 'price': 100})
        self.assertRedirects(response, reverse('fruit_list'))
        
        fruit = Fruit.objects.get(id = 2)
        self.assertEquals(fruit.name, 'リンゴ')
        self.assertEquals(fruit.price, 100)

    def test_fruit_update_view_post(self):
        url = reverse('fruit_edit', args=(1,))
        response = self.client.post(url, {'name': 'オレンジ', 'price':150})
        self.assertRedirects(response, reverse('fruit_list'))
        
        fruit = Fruit.objects.get(id = 1)
        self.assertEquals(fruit.name, 'オレンジ')
        self.assertEquals(fruit.price, 150)

    def test_fruit_delete_view_post(self):
        url = reverse('fruit_delete', args=(1,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('fruit_list'))

        with self.assertRaises(Fruit.DoesNotExist):
            Fruit.objects.get(id = 1)


class NoLoginFruitViewPostTest(TestCase):
    """非ログイン状態でCreate, Update, DeleteのPostをはじくかテスト"""
    def setUp(self):
        Fruit.objects.create(name='みかん', price=100)

    def test_fruit_create_view_post(self):
        url = reverse('fruit_new')
        response = self.client.post(url, {'name': 'リンゴ', 'price': 100})
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        
        self.assertEquals(len(Fruit.objects.all()), 1)

    def test_fruit_update_view_post(self):
        url = reverse('fruit_edit', args=(1,))
        response = self.client.post(url, {'name': 'オレンジ', 'price':150})
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        
        fruit = Fruit.objects.get(id = 1)
        self.assertEquals(fruit.name, 'みかん')
        self.assertEquals(fruit.price, 100)

    def test_fruit_delete_view_post(self):
        url = reverse('fruit_delete', args=(1,))
        response = self.client.post(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)

        fruit = Fruit.objects.get(id = 1)
        self.assertEquals(fruit.name, 'みかん')
        self.assertEquals(fruit.price, 100)