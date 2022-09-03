from django.test import TestCase
from django.urls import reverse
from django.test import TestCase
from mysite.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from django.contrib.auth import get_user_model, SESSION_KEY
from .models import Tweet


User = get_user_model()


class TestTweetCreateView(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="testpassword")
        self.client.login(username="testuser", password="testpassword")
        self.url = reverse("tweets:tweet_create")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_create.html")

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
            reverse("tweets:tweet_detail", kwargs={"pk": self.tweet.pk})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "tweets/tweet_detail.html")
        self.assertEquals(self.tweet, response.context["tweet"])


class TestTweetDeleteView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


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
