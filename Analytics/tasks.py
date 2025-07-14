from celery import shared_task
from Analytics.models import ProductAnalytics, TrafficLog, TrafficSourceAnalytics
from .models import ProductViewLog
from django.db.models import Count
from django.db.models import Q


@shared_task
def aggregate_product_views():
    logs = ProductViewLog.objects.values('product').annotate(view_count=Count('id'))
    for log in logs:
        obj, _ = ProductAnalytics.objects.get_or_create(product=log['product'])
        obj.total_views += log['view_count']
        obj.save()

    ProductViewLog.objects.all().delete()

@shared_task
def aggregate_traffic_sources():
    sources = TrafficLog.objects.values('source').annotate(
        visits=Count('id'),
        conversions=Count('id', filter=Q(converted=True)),
    )

    for s in sources:
        obj, _ = TrafficSourceAnalytics.objects.get_or_create(source=s['source'])
        obj.visits += s['visits']
        obj.conversions += s['conversions']
        obj.bounce_rate = 1 - (obj.conversions / obj.visits) if obj.visits else 0
        obj.save()

    TrafficLog.objects.all().delete()
