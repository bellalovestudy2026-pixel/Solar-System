from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):
    password = 'Orbit!Lantern92Telescope'

    def signup_data(self, **overrides):
        return {'username': 'student', 'password1': self.password,
                'password2': self.password, **overrides}

    def create_student(self):
        return get_user_model().objects.create_user('student', password=self.password)

    def test_guest_pages(self):
        for name in ('home', 'signup', 'login', 'science', 'solar_system'):
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(f'learning:{name}')).status_code, 200)
        response = self.client.get(reverse('learning:home'))
        self.assertContains(response, 'Sign up')
        self.assertNotContains(response, 'Log out')

    def test_signup_hashes_password_and_redirects_to_login(self):
        response = self.client.post(reverse('learning:signup'), self.signup_data())
        self.assertRedirects(response, reverse('learning:login'))
        student = get_user_model().objects.get(username='student')
        self.assertNotEqual(student.password, self.password)
        self.assertTrue(student.check_password(self.password))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_invalid_signup_does_not_create_user(self):
        for data in (self.signup_data(password2='different'),
                     self.signup_data(password1='123', password2='123'),
                     self.signup_data(username='')):
            with self.subTest(data=data):
                response = self.client.post(reverse('learning:signup'), data)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context['form'].errors)
                self.assertFalse(get_user_model().objects.exists())

    def test_duplicate_username_is_rejected(self):
        self.create_student()
        response = self.client.post(reverse('learning:signup'), self.signup_data())
        self.assertIn('username', response.context['form'].errors)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_login_shows_username_and_logout_clears_session(self):
        student = self.create_student()
        response = self.client.post(reverse('learning:login'),
                                    {'username': 'student', 'password': self.password})
        self.assertRedirects(response, reverse('learning:home'))
        self.assertEqual(self.client.session['_auth_user_id'], str(student.pk))
        response = self.client.get(reverse('learning:home'))
        self.assertContains(response, 'Welcome, student!')
        self.assertContains(response, 'Log out')
        self.assertNotContains(response, '>Sign up</a>')
        self.assertEqual(self.client.get(reverse('learning:logout')).status_code, 405)
        response = self.client.post(reverse('learning:logout'))
        self.assertRedirects(response, reverse('learning:home'))
        self.assertNotIn('_auth_user_id', self.client.session)
        self.assertNotContains(self.client.get(reverse('learning:home')), 'Welcome, student!')

    def test_invalid_login(self):
        self.create_student()
        response = self.client.post(reverse('learning:login'),
                                    {'username': 'student', 'password': 'wrong'})
        self.assertTrue(response.context['form'].non_field_errors())
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_next_allows_local_path_and_rejects_external_url(self):
        self.create_student()
        for target, expected in (('/science/', '/science/'),
                                 ('https://example.com/', reverse('learning:home'))):
            with self.subTest(target=target):
                response = self.client.post(reverse('learning:login'),
                    {'username': 'student', 'password': self.password, 'next': target})
                self.assertRedirects(response, expected)
                self.client.post(reverse('learning:logout'))

    def test_forms_require_csrf_and_valid_tokens_work(self):
        client = Client(enforce_csrf_checks=True)
        for name, data in (('signup', self.signup_data()),
                           ('login', {'username': 'student', 'password': self.password}),
                           ('logout', {})):
            self.assertEqual(client.post(reverse(f'learning:{name}'), data).status_code, 403)
        client.get(reverse('learning:signup'))
        response = client.post(reverse('learning:signup'), self.signup_data(
            csrfmiddlewaretoken=client.cookies['csrftoken'].value))
        self.assertRedirects(response, reverse('learning:login'))
        client.get(reverse('learning:login'))
        response = client.post(reverse('learning:login'), {
            'username': 'student', 'password': self.password,
            'csrfmiddlewaretoken': client.cookies['csrftoken'].value})
        self.assertRedirects(response, reverse('learning:home'))
        response = client.post(reverse('learning:logout'), {
            'csrfmiddlewaretoken': client.cookies['csrftoken'].value})
        self.assertRedirects(response, reverse('learning:home'))
