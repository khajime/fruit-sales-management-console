from fruitsales.models import Sale


def get_sales_filtered_sold_at(start_datetime, end_datetime, sales=None):
    """Saleテーブルから一定期間内のレコードを取得
    * salesを外部から与えた場合、その中から取得
    * salesが外部から与えられない場合、新たにall()で取得

    Args:
        start_date: 期間の始まり(inclusive)
        end_date: 期間の終わり(exclusive)
        sales: Saleオブジェクトのリスト
    Returns:
        一定期間内のレコードのリスト
    """
    if sales is None:
        sales = Sale.objects.all()

    sales_filtered = [sale for sale in sales
                    if (sale.sold_at >= start_datetime and sale.sold_at < end_datetime)]

    return sales_filtered


def cumulate_sales_fruitwise(start_datetime, end_datetime, sales=None):
    """Saleテーブルから果物ごとに一定期間内の累計売上・個数を計算
    * salesを外部から与えた場合、その中から集計

    Args:
        start_date: 期間の始まり(inclusive)
        end_date: 期間の終わり(exclusive)
        sales: Saleオブジェクトのリスト
    Returns:
        期間内の売り上げ累計, 果物ごとの集計値リスト
    """
    # sales = Sale.objects.filter(sold_at__gte=start_datetime,
    #                     sold_at__lt=end_datetime)
    sales = get_sales_filtered_sold_at(start_datetime, end_datetime, sales=sales)
    sales_amount = sum([sale.amount for sale in sales])

    # 果物ごとに集計
    result_dict = {}            
    for sale in sales:
        if sale.fruit.id in result_dict:
            result_dict[sale.fruit.id]['number'] += sale.number
            result_dict[sale.fruit.id]['amount'] += sale.amount
        else:
            result_dict[sale.fruit.id] = {'name': sale.fruit.name,
                                            'number': sale.number,
                                            'amount': sale.amount
                                        }

    return sales_amount, list(result_dict.values())