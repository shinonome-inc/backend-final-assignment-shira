from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Tweet
from accounts.models import Connection


User = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        connection = Connection(user=user)
        connection.save()
        self.client.login(username="testuser", password="testpassword")
        self.url = reverse("tweets:create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/create.html")

    def test_success_post(self):
        test_data = {"content": "testcontent"}
        response = self.client.post(self.url, test_data)
        self.assertRedirects(
            response,
            reverse("welcome:index"),
            status_code=302,
        )
        self.assertTrue(Tweet.objects.filter(content=test_data["content"]).exists())

    def test_failure_post_with_empty_content(self):
        empty_content_data = {"content": ""}
        response = self.client.post(self.url, empty_content_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "content",
            "このフィールドは必須です。",
        )
        self.assertFalse(Tweet.objects.exists())

    def test_failure_post_with_too_long_content(self):
        too_long_content_data = {"content": "a" * 141}
        response = self.client.post(self.url, too_long_content_data)
        self.assertEquals(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "content",
            "この値は 140 文字以下でなければなりません( 141 文字になっています)。",
        )
        self.assertFalse(Tweet.objects.exists())


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        connection = Connection(user=self.user)
        connection.save()
        self.client.login(
            username="testuser",
            password="testpassword",
        )
        self.tweet = Tweet.objects.create(
            user=self.user,
            content="testtweet",
        )

    def test_success_get(self):
        response = self.client.get(
            reverse("tweets:detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/detail.html")
        self.assertEquals(self.tweet, response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword1",
        )
        connection1 = Connection(user=self.user1)
        connection1.save()
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword2",
        )
        connection2 = Connection(user=self.user2)
        connection2.save()
        self.client.login(
            username="testuser1",
            password="testpassword1",
        )
        self.tweet1 = Tweet.objects.create(user=self.user1, content="testtweet1")
        self.tweet2 = Tweet.objects.create(user=self.user2, content="testtweet2")

    def test_success_post(self):
        response = self.client.post(
            reverse("tweets:delete", kwargs={"pk": self.tweet1.pk}),
        )
        self.assertRedirects(
            response,
            reverse("welcome:index"),
            status_code=302,
        )
        self.assertFalse(Tweet.objects.filter(content="testtweet1").exists())

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


class TestFavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_favorited_tweet(self):
        pass


class TestUnfavoriteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_unfavorited_tweet(self):
        pass
