from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model, SESSION_KEY
from django.conf import settings

from tweets.models import Tweet
from .models import Connection


User = get_user_model()


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.filter(username=data["username"]).exists())
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response,
            "form",
            "username",
            "このフィールドは必須です。",
        )

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response,
            "form",
            "username",
            "このフィールドは必須です。",
        )

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "testuser",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response,
            "form",
            "password2",
            "このフィールドは必須です。",
        )

    def test_failure_post_with_duplicated_user(self):
        existing_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, existing_data)

        new_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, new_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertFormError(
            response,
            "form",
            "username",
            "同じユーザー名が既に登録済みです。",
        )

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "testuser",
            "password1": "atre",
            "password2": "atre",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response,
            "form",
            "password2",
            "このパスワードは短すぎます。最低 8 文字以上必要です。",
        )

    def test_failure_post_with_password_similar_to_username(self):
        data = {
            "username": "testuser",
            "password1": "testuserpass",
            "password2": "testuserpass",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response,
            "form",
            "password2",
            "このパスワードは ユーザー名 と似すぎています。",
        )

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "testuser",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response,
            "form",
            "password2",
            ["このパスワードは一般的すぎます。", "このパスワードは数字しか使われていません。"],
        )

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "testuser",
            "password1": "testpassword1",
            "password2": "testpassword2",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response,
            "form",
            "password2",
            "確認用パスワードが一致しません。",
        )


class TestHomeView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        connection = Connection(user=self.user)
        connection.save()
        Tweet.objects.create(
            user=self.user,
            content="test_tweet1",
        )
        Tweet.objects.create(
            user=self.user,
            content="test_tweet2",
        )

    def test_success_get(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.get(reverse("welcome:index"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "welcome/index.html")
        self.assertQuerysetEqual(
            response.context["tweet_list"],
            Tweet.objects.order_by("created_at"),
        )


class TestLoginView(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        connection = Connection(user=user)
        connection.save()
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertRedirects(
            response,
            reverse(settings.LOGIN_REDIRECT_URL),
            status_code=302,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        data = {
            "username": "non_existing_user",
            "password": "testpassword",
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertFormError(
            response,
            "form",
            None,
            "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。",
        )

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertFormError(
            response,
            "form",
            "password",
            "このフィールドは必須です。",
        )


class TestLogoutView(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
        )
        connection = Connection(user=user)
        connection.save()
        self.url = reverse("accounts:logout")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(settings.LOGOUT_REDIRECT_URL),
            status_code=302,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.connection1 = Connection(user=self.user1)
        self.connection1.save()
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.connection2 = Connection(user=self.user2)
        self.connection2.save()
        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
        )
        self.connection3 = Connection(user=self.user3)
        self.connection3.save()
        self.connection1.following.add(self.user2)
        self.connection2.following.add(self.user3)

    def test_success_get(self):
        response1 = self.client.get(
            reverse("accounts:profile", kwargs={"username": self.user1.username})
        )
        self.assertEqual(
            response1.context["following_list"].count(),
            self.connection1.following.all().count(),
        )
        self.assertEqual(
            response1.context["follower_list"].count(),
            User.objects.filter(connection__following=self.user1).count(),
        )
        response2 = self.client.get(
            reverse("accounts:profile", kwargs={"username": self.user2.username})
        )
        self.assertEqual(
            response2.context["following_list"].count(),
            self.connection2.following.all().count(),
        )
        self.assertEqual(
            response2.context["follower_list"].count(),
            User.objects.filter(connection__following=self.user2).count(),
        )
        response3 = self.client.get(
            reverse("accounts:profile", kwargs={"username": self.user3.username})
        )
        self.assertEqual(
            response3.context["following_list"].count(),
            self.connection3.following.all().count(),
        )
        self.assertEqual(
            response3.context["follower_list"].count(),
            User.objects.filter(connection__following=self.user3).count(),
        )


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.connection1 = Connection(user=self.user1)
        self.connection1.save()
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.connection2 = Connection(user=self.user2)
        self.connection2.save()
        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
        )
        self.connection3 = Connection(user=self.user3)
        self.connection3.save()
        self.client.login(username="testuser1", password="testpassword")

    def test_success_post(self):
        response = self.client.get(
            reverse("accounts:follow", kwargs={"username": self.user2.username})
        )
        self.assertRedirects(
            response,
            reverse("welcome:index"),
            status_code=302,
        )
        self.assertTrue(Connection.objects.filter(following=self.user2).exists())

    def test_failure_post_with_not_exist_user(self):
        response = self.client.get(
            reverse("accounts:follow", kwargs={"username": "non_existing_usename"})
        )
        self.assertEquals(response.status_code, 404)
        self.assertFalse(User.objects.filter(connection__following=self.user1).exists())

    def test_failure_post_with_self(self):
        response = self.client.get(
            reverse("accounts:follow", kwargs={"username": self.user1.username})
        )
        self.assertEquals(response.status_code, 200)
        self.assertFalse(User.objects.filter(connection__following=self.user1).exists())


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.connection1 = Connection(user=self.user1)
        self.connection1.save()
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.connection2 = Connection(user=self.user2)
        self.connection2.save()
        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
        )
        self.connection3 = Connection(user=self.user3)
        self.connection3.save()
        self.connection1.following.add(self.user2)
        self.connection1.following.add(self.user3)
        self.client.login(username="testuser1", password="testpassword")

    def test_success_post(self):
        response = self.client.get(
            reverse("accounts:unfollow", kwargs={"username": self.user2.username})
        )
        self.assertRedirects(
            response,
            reverse("welcome:index"),
            status_code=302,
        )
        self.assertFalse(Connection.objects.filter(following=self.user2).exists())

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.get(
            reverse("accounts:unfollow", kwargs={"username": "non_existing_usename"})
        )
        self.assertEquals(response.status_code, 404)
        self.assertFalse(User.objects.filter(connection__following=self.user1).exists())

    def test_failure_post_with_incorrect_user(self):
        response = self.client.get(
            reverse("accounts:follow", kwargs={"username": self.user1.username})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTrue(Connection.objects.filter(following=self.user2).exists())
        self.assertTrue(Connection.objects.filter(following=self.user3).exists())


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.connection1 = Connection(user=self.user1)
        self.connection1.save()
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.connection2 = Connection(user=self.user2)
        self.connection2.save()
        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
        )
        self.connection3 = Connection(user=self.user3)
        self.connection3.save()
        self.connection1.following.add(self.user2)
        self.connection1.following.add(self.user3)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:following_list", kwargs={"username": self.user1.username})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/following_list.html")


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            password="testpassword",
        )
        self.connection1 = Connection(user=self.user1)
        self.connection1.save()
        self.user2 = User.objects.create_user(
            username="testuser2",
            password="testpassword",
        )
        self.connection2 = Connection(user=self.user2)
        self.connection2.save()
        self.user3 = User.objects.create_user(
            username="testuser3",
            password="testpassword",
        )
        self.connection3 = Connection(user=self.user3)
        self.connection3.save()
        self.connection1.following.add(self.user2)
        self.connection1.following.add(self.user3)

    def test_success_get(self):
        response = self.client.get(
            reverse("accounts:follower_list", kwargs={"username": self.user1.username})
        )
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/follower_list.html")
