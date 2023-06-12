##DUB
import warnings
import unittest
import boto3
from moto import mock_dynamodb
import sys
import os
import json

@mock_dynamodb
class TestDatabaseFunctions(unittest.TestCase):
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

        from src.todoList import create_todo_table
        self.table = create_todo_table(self.dynamodb)

    def tearDown(self):
        self.table.delete()
        self.dynamodb = None

    def test_table_exists(self):
        tableName = os.environ['DYNAMODB_TABLE']
        self.assertIn(tableName, self.table.name)

    def test_put_todo(self):
        from src.todoList import put_item
        response = put_item(self.text, self.dynamodb)
        self.assertEqual(200, response['statusCode'])

    def test_put_todo_error(self):
        from src.todoList import put_item
        with self.assertRaises(Exception):
            put_item("", self.dynamodb)

    def test_get_todo(self):
        from src.todoList import get_item, put_item
        responsePut = put_item(self.text, self.dynamodb)
        idItem = json.loads(responsePut['body'])['id']
        responseGet = get_item(idItem, self.dynamodb)
        self.assertEqual(self.text, responseGet['text'])

    def test_list_todo(self):
        from src.todoList import put_item, get_items
        put_item(self.text, self.dynamodb)
        result = get_items(self.dynamodb)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['text'], self.text)

    def test_update_todo(self):
        from src.todoList import put_item, update_item, get_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        responsePut = put_item(self.text, self.dynamodb)
        idItem = json.loads(responsePut['body'])['id']
        result = update_item(idItem, updated_text, "false", self.dynamodb)
        self.assertEqual(result['text'], updated_text)

    def test_update_todo_error(self):
        from src.todoList import put_item, update_item
        updated_text = "Aprender más cosas que DevOps y Cloud en la UNIR"
        responsePut = put_item(self.text, self.dynamodb)
        with self.assertRaises(Exception):
            update_item(updated_text, "", "false", self.dynamodb)
        with self.assertRaises(TypeError):
            update_item("", self.uuid, "false", self.dynamodb)
        with self.assertRaises(Exception):
            update_item(updated_text, self.uuid, "", self.dynamodb)

    def test_delete_todo(self):
        from src.todoList import delete_item, put_item, get_items
        responsePut = put_item(self.text, self.dynamodb)
        idItem = json.loads(responsePut['body'])['id']
        delete_item(idItem, self.dynamodb)
        self.assertEqual(len(get_items(self.dynamodb)), 0)

    def test_delete_todo_error(self):
        from src.todoList import delete_item
        with self.assertRaises(TypeError):
            delete_item("", self.dynamodb)

if __name__ == '__main__':
    unittest.main()
