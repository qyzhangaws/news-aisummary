from datetime import datetime
from calendar import c
import unittest
import datastore

class TestDynamoDBManager(unittest.TestCase):
    def setUp(self):
        self.region = 'us-west-2'
        self.table = 'test-news-aisummary'
        self.dynamodb_manager = datastore.DynamoDBManager(self.region, self.table)

    def test_dynamodb_manager(self):
        self.assertIsInstance(self.dynamodb_manager, datastore.DynamoDBManager)
        if not self.dynamodb_manager.is_table_exists():
            self.dynamodb_manager.create_table()

        self.dynamodb_manager.put_item(
            link='https://example.com/article2',
            title='Article 2',
            content='This is the content of article 2.',
            author='John Doe',
            publish_date='2024-07-02',
            website='example.com'
        )

        # Query items between dates
        start_date = datetime.fromisoformat('2024-07-01').date()
        end_date = datetime.fromisoformat('2024-07-03').date()
        items = self.dynamodb_manager.query_items_between_dates("example.com", start_date, end_date)
        print(len(items))
        print(items)

if __name__ == '__main__':
    unittest.main()
