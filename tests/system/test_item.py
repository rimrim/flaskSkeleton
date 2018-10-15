import json

from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test','password').save_to_db()
                auth_resp = client.post('/auth',
                                        data=json.dumps({'username':'test','password':'password'}),
                                        headers={'Content-Type':'application/json'})
                auth_token = json.loads(auth_resp.data)['access_token']
                self.access_token = f'JWT {auth_token}'


    def test_get_item_not_auth(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test')
                self.assertEqual(resp.status_code, 500)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/test',
                                  headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test store').save_to_db()
                ItemModel('test', 19, 1).save_to_db()
                resp = client.get('/item/test',
                                  headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 200)
