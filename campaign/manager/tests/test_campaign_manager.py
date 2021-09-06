from django.test import TestCase
from campaign.manager.campaign_manager import CampaignManager
from campaign.models import Campaign, Subscriber

class CampaignManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.campaign_manager = CampaignManager()
        return super().setUp()

    def test_add_subscriber_base_case(self):
        campaign = Campaign.objects.create(title='Test campaign', description='')
        subscriber_email = 'john@doe.com'
        subscriber_data = '{"name": "John", "last_name": "Doe"}'
        subscriber = self.campaign_manager.add_subscriber(
            campaign_id=campaign.id, 
            email=subscriber_email, 
            subscriber_data= subscriber_data
        )
        self.assertEqual(subscriber.__class__, Subscriber)
        self.assertEqual(subscriber.campaign.id, campaign.id)
        self.assertEqual(subscriber.email, subscriber_email)
        self.assertEqual(subscriber.user_data, subscriber_data)
        

    def test_add_subscriber_check_campaign_exists(self):
        with self.assertRaises(ValueError) as error:
            self.campaign_manager.add_subscriber(1, 'john@doe.com', '{}')
        
    
    