from turtle import title
from django.test import TestCase
from .models import Todo

class TodoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        Todo.objects.create(title='first todo', body='a body here')

    def test_title_content(self):
        todo = Todo.objects.get(id=1)
        expected_objects_name = f'{todo.title}'
        self.assertEqual(expected_objects_name, 'first todo')

    def test_body_content(self):
        todo = Todo.objects.get(id=1)
        expected_objects_name = f'{todo.body}'
        self.assertEqual(expected_objects_name, 'a body here')
