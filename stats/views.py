from django.shortcuts import render
from django.http import Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required


from dateutil.relativedelta import relativedelta
from fruitsales.models import Sale
from .utils import cumulate_sales_fruitwise


@login_required
def fruitsale_stats_view(request):
    if request.method == 'GET':
        # cumulate sales amount
        total_sales = sum([sale.amount for sale in Sale.objects.all()])

        # get current local time
        now = timezone.localtime()

        # for last 3 months
        monthly_sales = []
        for i in range(3):
            # TODO: filter by sold_at range, cumulate, create dict
            start_date = (now - relativedelta(months=i)).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + relativedelta(months=1)

            # 集計前にタイムゾーンをUTCに変換
            start_date = start_date.astimezone(timezone.utc)
            end_date = end_date.astimezone(timezone.utc)

            amount, detail = cumulate_sales_fruitwise(start_date, end_date)

            monthly_sales.append({'date': start_date, 'amount': amount, 'detail': detail})

        # for last 3 days
        daily_sales = []
        for i in range(3):
            # TODO: filter by sold_at range, cumulate, create dict
            start_date = (now - relativedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
            end_date = start_date + relativedelta(days=1)

            # 集計前にタイムゾーンをUTCに変換
            start_date = start_date.astimezone(timezone.utc)
            end_date = end_date.astimezone(timezone.utc)

            amount, detail = cumulate_sales_fruitwise(start_date, end_date)
            
            daily_sales.append({'date': start_date, 'amount': amount, 'detail': detail})

        return render(request, 'stats/fruitsale_stats.html',
                    {'total_sales': total_sales,
                    'monthly_sales': monthly_sales,
                    'daily_sales': daily_sales}
                    )
    else:
        raise Http404()