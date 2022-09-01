from django.shortcuts import render


def index_view(request):
    return render(request, "welcome/index.html")


"""
    if request.method == "GET":
        user_profile = Profile.objects.get(user=request.user)
        form = TweetForm()
        tweet_list = Tweet.objects.all().order_by("-id")
        favorited_tweet_id_list = request.user.favorite_account.values_list(
            "favorited_tweet_id", flat=True
        )
        return render(
            request,
            "account/home.html",
            {
                "profile": user_profile,
                "form": form,
                "tweet_list": tweet_list,
                "favorited_tweet_id_list": favorited_tweet_id_list,
            },
        )
    elif request.method == "POST":
        user_profile = Profile.objects.get(user=request.user)
        form = TweetForm(data=request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
        return redirect(reverse("account:home"))

    return HttpResponseNotAllowed(["GET", "POST"])"""
