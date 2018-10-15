from tests.base_test import BaseTest
from models.user import UserModel


class UserTest(BaseTest):
    def test_init_user(self):
        with self.app_context():
            user = UserModel('user', 'password')
            self.assertEqual('user', user.username)
            self.assertEqual('password', user.password)
            user.save_to_db()
            self.assertIsNotNone(UserModel.find_by_id(1))
            self.assertIsNotNone(UserModel.find_by_username('user'))
