from django.urls import reverse
from django.test import TestCase

from mysite.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from django.contrib.auth import get_user_model, SESSION_KEY

User = get_user_model()


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")  # type: ignore

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, data)

        self.assertRedirects(
            response,  # type: ignore
            reverse(LOGIN_REDIRECT_URL),
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
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")  # type: ignore

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response, "form", "username", "このフィールドは必須です。")  # type: ignore

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "testuser",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response, "form", "password2", "このフィールドは必須です。")  # type: ignore

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
        self.assertFormError(response, "form", "username", "同じユーザー名が既に登録済みです。")  # type: ignore

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "testuser",
            "password1": "test",
            "password2": "test",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(
            response, "form", "password2", "このパスワードは短すぎます。最低 8 文字以上必要です。"  # type: ignore
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
        self.assertFormError(response, "form", "password2", "このパスワードは ユーザー名 と似すぎています。")  # type: ignore

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "testuser",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response, "form", "password2", "このパスワードは一般的すぎます。")  # type: ignore

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "testuser",
            "password1": "testpassword1",
            "password2": "testpassword2",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 0)
        self.assertFormError(response, "form", "password2", "確認用パスワードが一致しません。")  # type: ignore


class TestHomeView(TestCase):
    def setUp(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.client.post(reverse("accounts:signup"), data)

    def test_success_get(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.get(reverse("accounts:home"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/home.html")  # type: ignore


class TestLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(username="testuser", password="testpassword")  # type: ignore
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")  # type: ignore

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertRedirects(
            response,  # type: ignore
            reverse(LOGIN_REDIRECT_URL),
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
            response, "form", "", "正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。"  # type: ignore
        )

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "testuser",
            "password": "",
        }
        response = self.client.post(reverse("accounts:login"), data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(SESSION_KEY, self.client.session)
        self.assertFormError(response, "form", "password", "このフィールドは必須です。")  # type: ignore


class TestLogoutView(TestCase):
    def setUp(self):
        data = {
            "username": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.client.post(reverse("accounts:signup"), data)
        self.url = reverse("accounts:logout")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,  # type: ignore
            reverse(LOGOUT_REDIRECT_URL),
            status_code=302,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


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
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
