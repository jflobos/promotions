
import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from campaign.models import Campaign, Subscriber
from campaign.views.add_subscriber import add_subscriber

class AddSubscriberTestCase(TestCase):
    multi_db=True

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.campaign = Campaign.objects.create(title='Test campaign', description='')
        self.subscriber_data = json.dumps({"name": "John", "last_name": "Doe"})

    def test_base_case(self):
        email = "john@doe.com"
        request = self.factory.post(
            '/subscriber/',
            {"email": email, "campaign_id": self.campaign.id, "subscriber_data": self.subscriber_data},
            format="json"
        )
        response = add_subscriber(request)
        self.assertEqual(response.status_code, 201)

    def test_base_should_create_a_subscriber(self):
        email = "john@doe.com"
        request = self.factory.post(
            '/subscriber/',
            {"email": email, "campaign_id": self.campaign.id, "subscriber_data": self.subscriber_data},
            format="json"
        )
        response = add_subscriber(request)
        self.assertEqual(response.status_code, 201)
        subscriber = Subscriber.objects.filter(campaign_id=self.campaign.id, email=email).first()
        self.assertEqual(subscriber.user_data, self.subscriber_data)

    def test_base_should_return_404_when_campaign_not_found(self):
        email = "john@doe.com"
        request = self.factory.post(
            '/subscriber/',
            {"email": email, "campaign_id": 5000, "subscriber_data": self.subscriber_data},
            format="json"
        )
        response = add_subscriber(request)
        self.assertEqual(response.status_code, 404)
    
    def test_base_should_return_400_when_email_is_repeated(self):
        email = "john@doe.com"
        request = self.factory.post(
            '/subscriber/',
            {"email": email, "campaign_id": self.campaign.id, "subscriber_data": self.subscriber_data},
            format="json"
        )
        add_subscriber(request)
        request = self.factory.post(
            '/subscriber/',
            {"email": email, "campaign_id": self.campaign.id, "subscriber_data": self.subscriber_data},
            format="json"
        )
        response = add_subscriber(request)
        self.assertEqual(response.status_code, 400)

