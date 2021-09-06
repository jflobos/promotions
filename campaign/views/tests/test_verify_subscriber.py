
import json
from rest_framework.test import APIRequestFactory
from django.test import TestCase
from campaign.models import Campaign, Subscriber
from campaign.manager.campaign_manager import CampaignManager
from campaign.views.verify_subscriber import verify_subscriber

class VerifySubscriberTestCase(TestCase):
    multi_db=True

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.campaign = Campaign.objects.create(title='Test campaign', description='')
        self.subscriber_data = json.dumps({"name": "John", "last_name": "Doe"})
        self.email = 'john@doe.com'
        campaign_manager = CampaignManager()
        self.subscriber = campaign_manager.add_subscriber(
            campaign_id=self.campaign.id,
            email=self.email,
            subscriber_data=self.subscriber_data
        )

    def test_base_case(self):
        request = self.factory.get(
            f'/subscriber/verify/?code={self.subscriber.verification_code}'
        )
        response = verify_subscriber(request)
        self.assertEqual(response.status_code, 200)

    def test_should_update_verified_field(self):
        request = self.factory.get(
            f'/subscriber/verify/?code={self.subscriber.verification_code}'
        )
        verify_subscriber(request)
        subscriber = Subscriber.objects.get(pk=self.subscriber.id)
        self.assertFalse(self.subscriber.verified)
        self.assertTrue(subscriber.verified)

    def test_should_throw_400_on_failure(self):
        request = self.factory.get(
            f'/subscriber/verify/?code=invalid_code'
        )
        response = verify_subscriber(request)
        self.assertEqual(response.status_code, 400)

