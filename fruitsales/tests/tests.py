import os


from django.test import TestCase
from django.core.exceptions import ValidationError


from .. import models
from fruits.models import Fruit


class CsvInputTest(TestCase):
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

        sales = models.generate_sales_from_csv(file)

        self.assertEqual(len(sales), 2)

    def test_invalid_csv_1(self):
        """日付フォーマットがおかしい場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records1.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = models.generate_sales_from_csv(file)
    
    def test_invalid_csv_2(self):
        """果物マスタに存在しない果物名を指定した場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records2.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = models.generate_sales_from_csv(file)

    def test_invalid_csv_3(self):
        """個数指定が負の場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records3.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = models.generate_sales_from_csv(file)

    def test_invalid_csv_4(self):
        """カンマ区切りの要素数が4でない場合、ValidationError"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records4.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = models.generate_sales_from_csv(file)

    def test_invalid_csv_5(self):
        """二つ目からのレコードのフォーマットがおかしい場合、一つ目のレコードは保存されない"""
        file = open(os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        'data/invalid_records5.csv'
                    ),
                    mode='rb'
                )

        with self.assertRaises(ValidationError):
            sales = models.generate_sales_from_csv(file)

        self.assertEqual(len(models.Sale.objects.all()), 0)