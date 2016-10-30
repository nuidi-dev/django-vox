from django.test import TestCase
from django.test import Client
from vox.models import Category, Topic
from django.contrib.auth.models import User

class VoxTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='test_user')
        test_user.set_password('test_321user')
        test_user.save()
        test_category = Category.objects.create(name='Test Category')
        Topic.objects.create(category=test_category, title='Test Topic!', author=test_user)

    # Get topics from API
    def test_visitor_can_get_topics_list_from_api(self):
        response = self.client.get('/api/topic', follow=True)
        self.assertEqual(response.status_code, 200, 'Cannot connect to Topic\'s API.')

    # User can log in
    def test_user_can_log_in(self):
        response = self.client.post('/login/', {'username': 'test_user', 'password': 'test_321user'}, follow=True)
        self.assertIn("Logout", response.content)


    # Visitor can get top rated topics
    # Visitor can get recent active topics

    # def test_user_can_create_new_topic(self):
    #     response = self.client.post('/api/topic/')
