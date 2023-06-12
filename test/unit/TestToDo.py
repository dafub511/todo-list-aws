##DUB
import warnings
import unittest
import boto3
from moto import mock_dynamodb
import os
import json

@mock_dynamodb
class TestTableExists(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")

    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        from src.todoList import create_todo_table
        self.table = create_todo_table(self.dynamodb)

    def tearDown(self):
        self.table.delete()
        self.dynamodb = None

    def test_table_exists(self):
        tableName = os.environ['DYNAMODB_TABLE']
        self.assertIn(tableName, self.table.name)

class TestTodoFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.filterwarnings(
            "ignore",
            category=ResourceWarning,
            message="unclosed.*<socket.socket.*>")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="callable is None.*")
        warnings.filterwarnings(
            "ignore",
            category=DeprecationWarning,
            message="Using or importing.*")

    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.uuid = "123e4567-e89b-12d3-a456-426614174000"
        self.text = "Aprender DevOps y Cloud en la UNIR"

        from src.todoList import create_todo_table, put_item
        self.table = create_todo_table(self.dynamodb)
        put_item(self.text, self.dynamodb)

    def tearDown(self):
        self.table.delete()
        self.dynamodb = None

    def test_put_todo(self):
        from src.todoList import put_item
        response = put_item(self.text, self.dynamodb)
        self.assertEqual(200, response['statusCode'])

    def test_put_todo_error(self):
        from src.todoList import put_item
        self.assertRaises(Exception, put_item, "", self.dynamodb)

    def test_get_todo(self):
        from src.todoList import get_item
        responseGet = get_item(self.uuid, self.dynamodb)
        self.assertEqual(self.text, responseGet['text'])

    def test_list_todo(self):
        from src.todoList import get_items
        result = get_items(self.dynamodb)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['text'], self.text)

    def test_update_todo(self):
        from src.todoList import update_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        result = update_item(self.uuid, updated_text, "false", self.dynamodb)
        self.assertEqual(result['text'], updated_text)

    def test_update_todo_error(self):
        from src.todoList import update_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        self.assertRaises(Exception, update_item, updated_text, "", "false", self.dynamodb)
        self.assertRaises(TypeError, update_item, "", self.uuid, "false", self.dynamodb)
        self.assertRaises(Exception, update_item, updated_text, self.uuid, "", self.dynamodb)

    def test_delete_todo(self):
        from src.todoList import delete_item, get_items
        delete_item(self.uuid, self.dynamodb)
        self.assertEqual(len(get_items(self.dynamodb)), 0)

    def test_delete_todo_error(self):
        from src.todoList import delete_item
        self.assertRaises(TypeError, delete_item, "", self.dynamodb)

if __name__ == '__main__':
    unittest.main()
