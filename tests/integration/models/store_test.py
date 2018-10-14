from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_item_empty(self):
        store = StoreModel('test')
        self.assertListEqual(store.items.all(), [], "items is not empty when creating store")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')
            self.assertIsNone(StoreModel.find_by_name('test'))
            store.save_to_db()
            self.assertIsNotNone(StoreModel.find_by_name('test'))
            store.delete_from_db()
            self.assertIsNone(StoreModel.find_by_name('test'))

    def test_relationship_with_item(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('testItem', 19, 1)
            store.save_to_db()
            item.save_to_db()
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'testItem')

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('testItem', 19, 1)
            store.save_to_db()
            item.save_to_db()
            expected = {
                'name':'test',
                'items': [
                    {
                        'name':'testItem',
                        'price':19
                    }
                ]
            }
            self.assertEqual(store.json(), expected)
