import unittest

from app.app import app, db
from app.endpoints import api
from app.models import Bucketlist, User, BucketlistItems



class BaseTestCase(unittest.TestCase):
    """Base test case class."""

    def setUp(self):
        self.app = app

        self.client = self.app.test_client
        self.user = {'name': 'testuser', 'password': 'testuser'}
        self.wrong_user = {'name': 'testuser_wrong', 'password': 'testuser_wrong'}

        with self.app.app_context():
            db.create_all()
            user = User(name="test_user", password="test_password")
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.session.commit()

    def authenticate(self):
        self.client().post('/api/v1/auth/register', data=self.user)
        req = self.client().post('/api/v1/auth/login', data=self.user)
        return req

if __name__ == "__main__":
    unittest.main()