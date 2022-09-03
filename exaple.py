class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testemail@email.com",
            password="testpassword",
        )
        self.client.login(username="testuser", password="testpassword")
        self.tweet = Tweet.objects.create(user=self.user, content="test_tweet")

    def test_success_get(self):
        response = self.client.get(
            reverse("tweets:detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_detail.html")
        self.assertEquals(self.tweet, response.context["tweet"])

    def test_success_get(self):
        User.objects.create_user(
            username="yamada", email="asaka@test.com", password="wasurenaide1108"
        )
        self.client.login(username="yamada", password="wasurenaide1108")
        data = {"contents": "頑張ってテストコードを書いています"}
        self.client.post(reverse("tweets:create"), data)
        tweet = Tweet.objects.get(contents="頑張ってテストコードを書いています")
        response_get = self.client.get(
            reverse("tweets:detail", kwargs={"pk": tweet.pk})
        )
        self.assertEquals(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, "tweets/tweets_detail.html")
        self.assertContains(response_get, data["contents"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="first_user",
            email="firstemail@email.com",
            password="first_password",
        )
        self.user2 = User.objects.create_user(
            username="second_user",
            email="secondemail@email.com",
            password="second_password",
        )
        self.client.login(username="first_user", password="first_password")
        self.tweet1 = Tweet.objects.create(user=self.user1, content="test_tweet")
        self.tweet2 = Tweet.objects.create(user=self.user2, content="test_tweet2")

    def test_success_post(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet1.pk})
        )
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertFalse(Tweet.objects.filter(content="test_tweet").exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 10}))
        self.assertEquals(response.status_code, 404)
        self.assertEquals(Tweet.objects.count(), 2)

    def test_failure_post_with_incorrect_user(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet2.pk})
        )
        self.assertEquals(response.status_code, 403)
        self.assertEquals(Tweet.objects.count(), 2)
