from flask import json

from tests.base_testcase import BaseTestCase


class TestBucketlistOperations(BaseTestCase):
    """Tests for bucketlist endpoints and operations."""

    # ENDPOINT: POST 'api/v1/bucketlist'
    def test_create_bucketlist(self):
        """Tests for correct bucketlist creation."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        req = self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.assertIn("Bucket list added successfully.", str(req.data))
        self.assertEqual(req.status_code, 201)

        req = self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.assertIn("Bucket list already exists!!.", str(req.data))
        self.assertEqual(req.status_code, 409)

        req = self.client().post('api/v1/bucketlist', headers=headers, data={})
        self.assertEqual(req.status_code, 400)

    # ENDPOINT: GET 'api/v1/bucketlist?q='bucket list one'
    def test_search_bucketlist(self):
        """Tests for viewing all bucketlists."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list one'})
        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list test'})

        req = self.client().get('api/v1/bucketlist?q=1', headers=headers)

        json_data = json.loads(req.data.decode(encoding='UTF-8'))

        self.assertEqual({'message': 'No results found!!'}, json_data)

        req = self.client().get('api/v1/bucketlist?q=one', headers=headers)

        json_data = json.loads(req.data.decode(encoding='UTF-8'))

        self.assertIn("Bucket list one", json_data['Bucket lists'][0]['description'])

    # ENDPOINT: GET 'api/v1/bucketlist?page=0
    def test_paginating_bucketlist(self):
        """Tests for viewing all bucketlists."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list one'})

        req = self.client().get('api/v1/bucketlist?page=1', headers=headers)

        json_data = json.loads(req.data.decode(encoding='UTF-8'))

        self.assertIn("Bucket list one", json_data['Bucket lists'][0]['description'])

    # ENDPOINT: GET 'api/v1/bucketlist'
    def test_view_all_bucketlist(self):
        """Tests for viewing all bucketlists."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})
        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example 2'})

        req = self.client().get('api/v1/bucketlist', headers=headers)

        json_data = json.loads(req.data.decode(encoding='UTF-8'))

        self.assertEqual('Bucket list example 1', json_data['Bucket lists'][0]['description'])
        self.assertEqual('Not available at the moment.', json_data['Bucket lists'][0]['items'])
        self.assertEqual('Bucket list example 2', json_data['Bucket lists'][1]['description'])
        self.assertEqual(req.status_code, 200)

    # ENDPOINT: GET 'api/v1/bucketlist/<int:id>'
    def test_view_individual_bucketlist(self):
        """Tests for viewing individual bucketlist."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().get('api/v1/bucketlist/1', headers=headers)

        json_data = json.loads(req.data.decode(encoding='UTF-8'))

        self.assertIn('Bucket list example 1', json_data['description'])
        self.assertEqual(req.status_code, 200)

    # ENDPOINT: GET 'api/v1/bucketlist/<int:id>'
    def test_view_none_existing_bucketlist(self):
        """Tests for viewing non existing bucketlist."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().get('api/v1/bucketlist/8', headers=headers)

        self.assertIn('message": "Bucketlist does not exist!!', str(req.data))
        self.assertEqual(req.status_code, 404)

    # ENDPOINT: DELETE 'api/v1/bucketlist/<int:id>'
    def test_delete_bucketlist(self):
        """Tests for deletion of a bucketlist."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().delete('api/v1/bucketlist/1', headers=headers)
        self.assertIn('message": "Bucket list deleted successfully!!', str(req.data))

    # ENDPOINT: PUT 'api/v1/bucketlist/<int:id>'
    def test_update_bucketlist(self):
        """Tests updating an existing bucketlist."""

        req = self.authenticate()
        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example 1'})

        req = self.client().put('api/v1/bucketlist/1', headers=headers, data={'desc': 'Bucket list example 1',
                                                                        'status': True})

        self.assertIn('message": "Bucket list changes made successfully.', str(req.data))
        self.assertEqual(req.status_code, 200)
