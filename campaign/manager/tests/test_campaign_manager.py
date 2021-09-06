from django.test import TestCase
from django.core.validators import ValidationError
from campaign.manager.campaign_manager import CampaignManager
from campaign.models import Campaign, Subscriber

class CampaignManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.campaign = Campaign.objects.create(title='Test campaign', description='')
        self.campaign_manager = CampaignManager()
        self.subscriber_email = 'john@doe.com'
        self.subscriber_data = '{"name": "John", "last_name": "Doe"}'
        return super().setUp()

    def test_add_subscriber_base_case(self):
        subscriber = self.campaign_manager.add_subscriber(
            campaign_id=self.campaign.id, 
            email=self.subscriber_email, 
            subscriber_data= self.subscriber_data
        )
        self.assertEqual(subscriber.__class__, Subscriber)
        self.assertEqual(subscriber.campaign.id, self.campaign.id)
        self.assertEqual(subscriber.email, self.subscriber_email)
        self.assertEqual(subscriber.user_data, self.subscriber_data)
        

    def test_add_subscriber_check_campaign_exists(self):
        with self.assertRaises(ValueError) as error:
            self.campaign_manager.add_subscriber(300, self.subscriber_email, self.subscriber_data)
        
    def test_add_subscriber_check_valid_email(self):
        invalid_email = 'johndoe.com'
        with self.assertRaises(ValidationError) as error:
            self.campaign_manager.add_subscriber(self.campaign.id, invalid_email, self.subscriber_data)
    
    def test_add_subscriber_cannot_replicate_email(self):
        repeteated_email = 'john+01@doe.com'
        self.campaign_manager.add_subscriber(
            campaign_id=self.campaign.id, 
            email=repeteated_email, 
            subscriber_data= self.subscriber_data
        )
        with self.assertRaises(ValueError): 
            self.campaign_manager.add_subscriber(
                campaign_id=self.campaign.id, 
                email=repeteated_email, 
                subscriber_data= self.subscriber_data
            )

