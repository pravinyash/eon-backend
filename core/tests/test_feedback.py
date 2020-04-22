"""
Test for feedback module api added here
"""
import json

from django.urls import reverse
from rest_framework.test import APITestCase

from authentication.models import Role, User
from core.models import Event, EventType, Question


class FeedbackQuestionsTestCase(APITestCase):
    """
    Test cases are created in this class
    """
    def setUp(cls):
        """
        Setup for Feedback Questions GET Api
        """
        role = Role(role="organizer")
        role.save()
        content = {
            "email": "user21@gmail.com",
            "name": "user21@gmail.com",
            "password": "user123",
            "contact": "9999911111",
            "address": "Bangalore",
            "role": "organizer",
            "organization": "Eventhigh"
        }

        cls.client.post('/authentication/registration', json.dumps(content),
                        content_type='application/json')
        data = dict(email="user21@gmail.com", password="user123")
        login_response = cls.client.post('/authentication/login', json.dumps(data),
                                         content_type='application/json')
        cls.user_id = login_response.data['data']['user']['user_id']
        cls.token = login_response.data['data']['access']
        cls.end_point = "/core/feedback-questions/"

    def test_feedback_questions_api_with_wrong_method_type(self):
        """
        Test Feedback questions api with wrong method name
        """
        response = self.client.put(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format(self.token)
        )
        self.assertEquals(response.status_code, 405)

    def test_feedback_questions_api_with_wrong_token(self):
        """
        Test Feedback questions api with wrong method name
        """
        response = self.client.put(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format('token')
        )
        self.assertEquals(response.status_code, 401)

    def test_get_api_for_feedback_questions(self):
        """
            Test Feedback questions api
        """
        response = self.client.get(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format(self.token)
        )
        self.assertEquals(response.status_code, 200)


class FeedbackTestCase(APITestCase):
    """
    Test cases are created in this class
    """

    def setUp(cls):
        """
        Setup for Feedback GET/POST APIs
        """
        role1 = Role(role="organizer")
        role1.save()
        role2 = Role(role="subscriber")
        role2.save()
        content1 = {
            "email": "user21@gmail.com",
            "name": "user21@gmail.com",
            "password": "user123",
            "contact": "9999911111",
            "address": "Bangalore",
            "role": "organizer",
            "organization": "Eventhigh"
        }
        content2 = {
            "email": "user20@gmail.com",
            "name": "user20@gmail.com",
            "password": "user123",
            "contact": "9999911111",
            "address": "Bangalore",
            "role": "subscriber",
            "organization": "Eventhigh"
        }

        cls.client.post('/authentication/registration', json.dumps(content1),
                        content_type='application/json')
        cls.client.post('/authentication/registration', json.dumps(content2),
                        content_type='application/json')
        data = dict(email="user20@gmail.com", password="user123")
        login_response = cls.client.post('/authentication/login', json.dumps(data),
                                         content_type='application/json')
        cls.user_id = login_response.data['data']['user']['user_id']
        cls.token = login_response.data['data']['access']
        cls.end_point = "/core/feedback/"

        cls.event_type = EventType(type="test")
        cls.event_type.save()

        cls.event = Event(name="test_event", type=cls.event_type, description="New Event",
                          date="2020-04-02",
                          time="12:38:00", location="karnal", subscription_fee=499,
                          no_of_tickets=250,
                          images="https://www.google.com/images", sold_tickets=0,
                          external_links="google.com",
                          event_created_by_id=User.objects.filter()[0].id)
        cls.event.save()
        cls.question = Question(question="Demo question1 ?")
        cls.question.save()

    def test_feedback_api_with_wrong_method_type(self):
        """
        Test Feedback api with wrong method name
        """
        data = dict(email="user20@gmail.com", password="user123")
        login_response = self.client.post('/authentication/login', json.dumps(data),
                                         content_type='application/json')
        user_id = login_response.data['data']['user']['user_id']
        token = login_response.data['data']['access']
        response = self.client.put(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format(token)
        )
        self.assertEquals(response.status_code, 405)

    def test_feedback_api_with_wrong_token(self):
        """
        Test Feedback api with wrong token
        """
        response = self.client.get(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format('token')
        )
        self.assertEquals(response.status_code, 401)

    def test_feedback_post_api_with_no_question_id(self):
        """
        Test Feedback api for post api with no question id
        """
        json_content = {
            "event_id": self.event.id,
            "feedback": [{
                "answer": {
                    "description": "abcd",
                    "image": "demo.jpeg"
                }
            }]
        }
        response = self.client.post(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format(self.token), data=json.dumps(json_content),
            content_type="application/json"
        )
        self.assertEquals(response.status_code, 400)

    def test_feedback_post_api_with_wrong_question_id(self):
        """
        Test Feedback api for post api with wrong question id
        """
        json_content = {
            "event_id": self.event.id,
            "feedback": [{
                "answer": {
                    "id": 100,
                    "description": "abcd",
                    "image": "demo.jpeg"
                }
            }]
        }
        response = self.client.post(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format(self.token), data=json.dumps(json_content),
            content_type="application/json"
        )
        self.assertEquals(response.status_code, 400)

    def test_feedback_post_api_with_correct_data(self):
        """
        Test Feedback api for post api
        """
        json_content = {
            "event_id": self.event.id,
            "feedback": [{
                "id": self.question.id,
                "answer": {
                    "description": "abcd",
                    "image": "demo.jpeg"
                }
            }]
        }
        response = self.client.post(
            self.end_point, HTTP_AUTHORIZATION="Bearer {}".format(self.token), data=json.dumps(json_content),
            content_type="application/json"
        )
        self.assertEquals(response.status_code, 200)

    def test_feedback_get_api_with_subscriber_login(self):
        """
        Test Feedback api for get with subscriber login
        """
        response = self.client.get(
            self.end_point+'?event_id={}'.format(self.event.id),
            HTTP_AUTHORIZATION="Bearer {}".format(self.token),
            content_type="application/json"
        )
        self.assertEquals(response.status_code, 200)

    def test_feedback_get_api_with_organizer_login(self):
        """
        Test Feedback api for get with organizer login
        """
        data = dict(email="user21@gmail.com", password="user123")
        login_response = self.client.post('/authentication/login', json.dumps(data),
                                          content_type='application/json')
        self.token = login_response.data['data']['access']
        response = self.client.get(
            self.end_point+'?event_id={}'.format(self.event.id),
            HTTP_AUTHORIZATION="Bearer {}".format(self.token),
            content_type="application/json"
        )
        self.assertEquals(response.status_code, 200)

    def test_feedback_get_api_with_no_event_in_parameter(self):
        """
        Test Feedback api for get with no event id as parameter
        """
        response = self.client.get(
            self.end_point,
            HTTP_AUTHORIZATION="Bearer {}".format(self.token),
            content_type="application/json"
        )
        self.assertEquals(response.status_code, 400)

    def test_feedback_get_api_with_wrong_event(self):
        """
        Test Feedback api for get with wrong event id
        """
        response = self.client.get(
            self.end_point+'?event_id={}'.format(100),
            HTTP_AUTHORIZATION="Bearer {}".format(self.token),
            content_type="application/json"
        )
        self.assertEquals(response.status_code, 400)
