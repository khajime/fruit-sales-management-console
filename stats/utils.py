from fruitsales.models import Sale


def cumulate_sales_fruitwise(start_date, end_date):
    """Saleテーブルから果物ごとに一定期間内の累計売上・個数を計算

    Args:
        start_date: 期間の始まり(inclusive)
        end_date: 期間の終わり(exclusive)
    Returns:
        期間内の売り上げ累計, 果物ごとの集計値
    """
    sales = Sale.objects.filter(sold_at__gte=start_date,
                        sold_at__lt=end_date)
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

    return sales_amount, result_dict.values()