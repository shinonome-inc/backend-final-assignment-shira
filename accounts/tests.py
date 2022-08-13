from django.urls import reverse
from django.test import TestCase

from mysite.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from .forms import SignupForm
from .models import CustomUser
from django.contrib.auth import get_user_model, SESSION_KEY

User = get_user_model()


class TestSignUpView(TestCase):
    def test_success_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/signup.html")  # type: ignore

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(reverse("signup"), data)

        self.assertRedirects(
            response,  # type: ignore
            reverse(LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )

        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 1)

        self.assertTrue(CustomUser.objects.filter(username=data["username"]).exists())

        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 0)
        f = SignupForm(data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["username"][0], "このフィールドは必須です。")

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 0)
        f = SignupForm(data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["username"][0], "このフィールドは必須です。")

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "testuser",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 0)
        f = SignupForm(data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password1"][0], "このフィールドは必須です。")
        self.assertEqual(f.errors["password2"][0], "このフィールドは必須です。")

    def test_failure_post_with_duplicated_user(self):
        existing_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(reverse("signup"), existing_data)

        new_data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(reverse("signup"), new_data)

        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 1)
        f = SignupForm(new_data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["username"][0], "同じユーザー名が既に登録済みです。")

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "testuser",
            "password1": "test",
            "password2": "test",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 0)
        f = SignupForm(data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "このパスワードは短すぎます。最低 8 文字以上必要です。")

    def test_failure_post_with_password_similar_to_username(self):
        data = {
            "username": "testuser",
            "password1": "testuserpass",
            "password2": "testuserpass",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 0)
        f = SignupForm(data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "このパスワードは ユーザー名 と似すぎています。")

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "testuser",
            "password1": "12345678",
            "password2": "12345678",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 0)
        f = SignupForm(data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "このパスワードは一般的すぎます。")

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "testuser",
            "password1": "testpassword1",
            "password2": "testpassword2",
        }
        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, 200)
        saved_accounts = CustomUser.objects.count()
        self.assertEqual(saved_accounts, 0)
        f = SignupForm(data)
        self.assertEqual(f.is_valid(), False)
        self.assertEqual(f.errors["password2"][0], "確認用パスワードが一致しません。")


class TestHomeView(TestCase):
    def setUp(self):
        data = {
            "username": "testuser",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        self.client.post(reverse("signup"), data)

    def test_success_get(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.get(reverse("home"), data)
        self.assertEqual(response.status_code, 200)


class TestLoginView(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(username="testuser", password="testpassword")  # type: ignore
        self.url = reverse("login")

    def test_success_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "testuser",
            "password": "testpassword",
        }
        response = self.client.post(reverse("login"), data)

        self.assertRedirects(
            response,  # type: ignore
            reverse(LOGIN_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
        )

        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        data = {
            "username": "non_existing_user",
            "password": "testpassword",
        }
        response = self.client.post(reverse("login"), data)

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
        response = self.client.post(reverse("login"), data)

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
        self.client.post(reverse("signup"), data)

    def test_success_get(self):
        response = self.client.get(reverse("logout"))
        self.assertRedirects(
            response,  # type: ignore
            reverse(LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
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
