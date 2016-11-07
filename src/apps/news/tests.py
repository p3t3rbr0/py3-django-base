from django.test import TestCase
from .models import Category, Tag


class CategoryTestCase(TestCase):
    def setUp(self):
        self.t_category = Category.objects.create(title='Новая категория', slug='new_category')

    def test_is_instance(self):
        self.assertTrue(isinstance(self.t_category, Category))
        self.assertEqual(self.t_category.__str__(), self.t_category.title)


class TagTestCase(TestCase):
    def setUp(self):
        self.t_tag = Tag.objects.create(title='new tag', slug='new_tag')

    def test_is_instance(self):
        self.assertTrue(isinstance(self.t_tag, Tag))
        self.assertEqual(self.t_tag.__str__(), self.t_tag.title)


class GetNewsDetailTest(TestCase):
    def setUp(self):
        pass

    def test_is_instance(self):
        pass
