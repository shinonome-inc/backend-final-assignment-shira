from django.shortcuts import render
from django.views.decorators.http import require_GET

from tweets.models import Tweet


@require_GET
def index_view(request):
    tweet_list = Tweet.objects.all().order_by("created_at")
    context = {"tweet_list": tweet_list}
    return render(request, "welcome/index.html", context)
