from base64 import b64encode

from flask import json

from tests.base_testcase import BaseTestCase


class TestUserAuth(BaseTestCase):
    """Tests for correct user authentiaction."""

    # ENDPOINT: POST '/auth/register'
    def test_user_registration(self):
        """Tests for correct user registration."""

        req = self.client().post('/auth/register')

        self.assertEqual(req.status_code, 401)

        req = self.client().post('/auth/register', data=self.user)

        self.assertEqual(req.status_code, 201)

        self.assertIn('Registration successful.', str(req.data))

        req = self.client().post('/auth/register', data={})
        self.assertIn('Provide your name and password!!', str(req.data))

    # ENDPOINT: POST '/auth/register'
    def test_registration_for_exististing_user(self):
        """Tests for user registration with existing username."""
        req = self.client().post('/auth/register', data=self.user)
        self.assertEqual(req.status_code, 201)

        same_user = self.user
        req = self.client().post('/auth/register', data=same_user)
        self.assertNotEqual(req.status_code, 201)

        self.assertIn('Username taken!!', str(req.data))

    # ENDPOINT: POST '/auth/login'
    def test_for_user_login(self):
        """Tests for correct user login."""

        req = self.client().post('/auth/register', data=self.user)
        self.assertEqual(req.status_code, 201)

        req = self.client().post('/auth/login', data=self.user)

        self.assertIn("testuser", str(req.data))

        req = self.client().post('/auth/login', data=self.wrong_user)
        self.assertIn("Wrong credentials!!", str(req.data))

    # ENDPOINT: GET '/auth/logout'
    def test_for_user_logout(self):
        """Tests for correct user logout."""
        self.client().post('/auth/register', data=self.user)
        req = self.client().post('/auth/login', data=self.user)

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token }

        req = self.client().get('/auth/logout', headers=headers)
        self.assertEqual(req.status_code, 200)
        self.assertIn('message": "You have successfully logged out.', str(req.data))
        req = self.client().get('/auth/logout', headers=headers)
        self.assertEqual(req.status_code, 403)
        self.assertIn('message": "You are not logged in. Please login!!!', str(req.data))


