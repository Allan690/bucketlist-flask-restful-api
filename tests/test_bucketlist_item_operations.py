from base64 import b64encode

from flask import json

from tests.base_testcase import BaseTestCase


class TestBucketListItemsOperations(BaseTestCase):
    """Tests for bucketlist items endpoints and operations."""

    # ENDPOINT: POST 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_create_bucketlist_items(self):
        """Tests for correct bucketlist item creation."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        req = self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My first goals"})

        self.assertEqual(req.status_code, 201)
        self.assertIn('message": "Bucket list item added successfully!!', str(req.data))

    # ENDPOINT: POST 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_create_bucketlist_item_with_existing_name(self):
        """Test for creation of bucketlist item with existing name."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My first goal"})
        req = self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My first goal"})
        self.assertIn('message": "Bucket list item already exists!!', str(req.data))

    # ENDPOINT: POST 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_create_bucket_list_item_with_empty_description(self):
        """Tests creation of bucketlist item with null description."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        req = self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': ""})
        self.assertIn('message": "goal cannot be empty!!', str(req.data))

    # ENDPOINT: GET 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_view_all_bucketlist_items(self):
        """Tests viewing all bucketlist items belonging to a single bucketlist."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My first goal"})
        self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My second goal"})

        req = self.client().get('api/v1/bucketlist/1/items', headers=headers)

        self.assertIn('goal": "My first goal', str(req.data))
        self.assertEqual(req.status_code, 200)
        self.assertIn('goal": "My second goal', str(req.data))
        self.assertEqual(req.status_code, 200)

    # ENDPOINT: GET 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_view_individual_bucket_list_item(self):
        """Tests for viewing a single bucketlist item."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My first goal"})

        req = self.client().get('api/v1/bucketlist/1/items/1', headers=headers)

        self.assertIn('goal": "My first goal', str(req.data))
        self.assertEqual(req.status_code, 200)

    # ENDPOINT: GET 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_view_non_existing_bucket_list_item(self):
        """Tests for viewing none existing bucketlist item."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})

        req = self.client().get('api/v1/bucketlist/1/items/12', headers=headers)

        self.assertIn('message": "Bucketlist item does not exists!!', str(req.data))
        self.assertEqual(req.status_code, 404)

    # ENDPOINT: DELETE 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_deletion_of_an_individual_bucket_list_item(self):
        """Tests for deletion of an individual bucketlist item."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My first goal"})

        req = self.client().delete('api/v1/bucketlist/1/items/1', headers=headers)

        self.assertIn('message": "Bucket list item deleted successfully', str(req.data))
        self.assertEqual(req.status_code, 200)

    # ENDPOINT: PUT 'api/v1/bucketlist/<int:id>/items/<int:item_id>'
    def test_change_completion_status_of_an_individual_bucket_list_item(self):
        """Tests for changing completion status of an individual bucketlist item."""

        req = self.authenticate()

        get_json = json.loads(req.data)
        token = get_json.get('token')

        headers = {'token': token}

        self.client().post('api/v1/bucketlist', headers=headers, data={'desc': 'Bucket list example'})
        self.client().post('api/v1/bucketlist/1/items', headers=headers, data={'goal': "My first goal"})

        req = self.client().put('api/v1/bucketlist/1/items/1', headers=headers)

        self.assertIn('message": "Goal completed.', str(req.data))
        self.assertEqual(req.status_code, 201)

