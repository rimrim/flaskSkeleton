import json

from models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username':'user', 'password':'1234'})
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_id(1))
                self.assertIsNotNone(UserModel.find_by_username('user'))
                self.assertDictEqual({'message':'User created successfully'},
                                     json.loads(response.data))

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/register', data={'username':'user', 'password':'1234'})
                self.assertEqual(response.status_code, 201)
                response = client.post('/register', data={'username':'user', 'password':'1234'})
                self.assertEqual(response.status_code, 400)

    # def test_register_and_login(self):
    #     with self.app() as client:
    #         with self.app_context():
    #             response = client.post('/register', data={'username':'user', 'password':'1234'})
    #             # /auth only accept json, not form
    #             auth_response = client.post('/auth',
    #                                        data=json.dumps({'username':'user','password':'1234'}),
    #                                        headers={'Content-Type': 'application/json'})
    #             self.assertIn('access_token', json.loads(auth_response.data).keys())

    def test_get_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/user/1')
                self.assertEqual(response.status_code, 404)
                UserModel('test','test').save_to_db()
                response = client.get('/user/1')
                self.assertEqual(response.status_code, 200)
                response = client.delete('/user/1')
                self.assertEqual(response.status_code, 200)
                response = client.get('/user/1')
                self.assertEqual(response.status_code, 404)

    def test_user_login(self):
        with self.app() as client:
            with self.app_context():
                UserModel('test','test').save_to_db()
                resp = client.post('/auth',
                                   data=json.dumps({'username':'test', 'password':'test'}),
                                   headers={'Content-Type': 'application/json'})
                self.assertIn('access_token', json.loads(resp.data).keys())
                self.assertIn('refresh_token', json.loads(resp.data).keys())

    def test_user_login_wrong_password(self):
        with self.app() as client:
            with self.app_context():
                UserModel('test','test').save_to_db()
                resp = client.post('/auth',
                                   data=json.dumps({'username':'test', 'password':'test2'}),
                                   headers={'Content-Type': 'application/json'})
                self.assertNotIn('access_token', json.loads(resp.data).keys())
                self.assertNotIn('refresh_token', json.loads(resp.data).keys())
                self.assertEqual(resp.status_code, 401)
