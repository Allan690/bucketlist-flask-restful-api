from flask import json

from tests.base_testcase import BaseTestCase


class TestBucketlistOperations(BaseTestCase):
    """Tests for bucketlist endpoints and operations."""

    # ENDPOINT: POST '/bucketlist'
    def test_create_bucketlist(self):
        """Tests for correct bucketlist creation."""

        self.client().post('/auth/register', data=self.user)
        req = self.client().post('/auth/login', data=self.user)
        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        req = self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.assertIn("Bucket list added successfully.", str(req.data))
        self.assertEqual(req.status_code, 201)

        req = self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.assertIn("Bucket list already exists!!.", str(req.data))
        self.assertEqual(req.status_code, 409)

        req = self.client().post('/bucketlist', headers=headers, data={})
        self.assertEqual(req.status_code, 204)

    # ENDPOINT: GET '/bucketlist'
    def test_view_all_bucketlist(self):
        """Tests for viewing all bucketlists."""

        self.client().post('/auth/register', data=self.user)
        req = self.client().post('/auth/login', data=self.user)
        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})
        self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example 2'})

        req = self.client().get('/bucketlist', headers=headers)

        json_data = json.loads(req.data.decode(encoding='UTF-8'))

        self.assertEqual('Bucket list example 1', json_data['Bucket lists'][0]['description'])
        self.assertEqual('Bucket list example 2', json_data['Bucket lists'][1]['description'])
        self.assertEqual(req.status_code, 200)

    # ENDPOINT: GET '/bucketlist/<int:id>'
    def test_view_individual_bucketlist(self):
        """Tests for viewing individual bucketlist."""

        self.client().post('/auth/register', data=self.user)
        req = self.client().post('/auth/login', data=self.user)
        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().get('/bucketlist/1', headers=headers)

        json_data = json.loads(req.data.decode(encoding='UTF-8'))

        self.assertIn('Bucket list example 1', json_data['description'])
        self.assertEqual(req.status_code, 200)

    # ENDPOINT: GET '/bucketlist/<int:id>'
    def test_view_none_existing_bucketlist(self):
        """Tests for viewing non existing bucketlist."""

        self.client().post('/auth/register', data=self.user)
        req = self.client().post('/auth/login', data=self.user)
        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().get('/bucketlist/8', headers=headers)

        self.assertIn('message": "Bucketlist does not exist!!', str(req.data))
        self.assertEqual(req.status_code, 404)

    # ENDPOINT: DELETE '/bucketlist/<int:id>'
    def test_delete_bucketlist(self):
        """Tests for deletion of a bucketlist."""

        self.client().post('/auth/register', data=self.user)
        req = self.client().post('/auth/login', data=self.user)
        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().delete('/bucketlist/1', headers=headers)
        self.assertIn('message": "Bucket list deleted successfully!!', str(req.data))

    # ENDPOINT: PUT '/bucketlist/<int:id>'
    def test_update_bucketlist(self):
        """Tests updating an existing bucketlist."""

        self.client().post('/auth/register', data=self.user)
        req = self.client().post('/auth/login', data=self.user)
        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().put('/bucketlist/1', headers=headers, data={'desc': 'Bucket list example 1',
                                                                        'status': True})

        self.assertIn('message": "Bucket list changes made successfully.', str(req.data))
        self.assertEqual(req.status_code, 200)
