from campaign.manager.exceptions import InvalidCampaignError, RepeatedEmailError
import json
from django.core.signing import Signer
from django.test import TestCase
from django.core.validators import ValidationError
from campaign.manager.campaign_manager import CampaignManager
from campaign.models import Campaign, Subscriber

class CampaignManagerTestCase(TestCase):
    multi_db=True
    def setUp(self) -> None:
        self.campaign = Campaign.objects.create(title='Test campaign', description='')
        self.campaign_manager = CampaignManager()
        self.subscriber_email = 'john@doe.com'
        self.subscriber_data = '{"name": "John", "last_name": "Doe"}'
        self.subscriber_verification_code = self.__get_verification_code(self.subscriber_email, self.campaign.id)
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
        self.assertFalse(subscriber.verified)
        self.assertEqual(subscriber.verification_code, self.subscriber_verification_code)

    def test_add_subscriber_check_campaign_exists(self):
        with self.assertRaises(InvalidCampaignError) as error:
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
        with self.assertRaises(RepeatedEmailError): 
            self.campaign_manager.add_subscriber(
                campaign_id=self.campaign.id, 
                email=repeteated_email, 
                subscriber_data= self.subscriber_data
            )

    def test_verify_email_base_case(self):
        email = "john+02@doe.com"
        self.campaign_manager.add_subscriber(
            campaign_id=self.campaign.id, 
            email=email, 
            subscriber_data=self.subscriber_data
        )
        verification_code = self.__get_verification_code(email=email, campaign_id=self.campaign.id)
        value = self.campaign_manager.verify_email(verification_code=verification_code)
        self.assertTrue(value)
    
    def test_verify_email_should_update_user_verify_field(self):
        email = "john+03@doe.com"
        subscriber = self.campaign_manager.add_subscriber(
            campaign_id=self.campaign.id, 
            email=email, 
            subscriber_data=self.subscriber_data
        )
        self.assertFalse(subscriber.verified)
        verification_code = self.__get_verification_code(email=email, campaign_id=self.campaign.id)
        value = self.campaign_manager.verify_email(verification_code=verification_code)
        self.assertTrue(value)
        updated_subscriber = Subscriber.objects.get(pk=subscriber.pk)
        self.assertTrue(updated_subscriber.verified)

    def test_finish_campaign_base_case(self):
        not_veriefed_emails = [
            "john+04@doe.com",
            "john+05@doe.com",
            "john+06@doe.com",
        ]
        for email in not_veriefed_emails:
            self.campaign_manager.add_subscriber(
                campaign_id=self.campaign.id, 
                email=email, 
                subscriber_data=self.subscriber_data
            )
        winner_email = "john+winner@doe.com"
        winner = self.campaign_manager.add_subscriber(
            campaign_id=self.campaign.id, 
            email=winner_email, 
            subscriber_data=self.subscriber_data
        )
        self.campaign_manager.verify_email(verification_code=winner.verification_code)
        self.campaign_manager.finish_campaign(self.campaign.id)
        updated_campaign = Campaign.objects.get(pk=self.campaign.id)
        self.assertEqual(updated_campaign.winner, winner.id)
        self.assertTrue(updated_campaign.finished)
    
    def test_finish_campaign_should_fail_with_no_subscribers(self):
        campaign = Campaign.objects.create(title="Empty campaign", description="")
        with self.assertRaises(ValueError):
            self.campaign_manager.finish_campaign(campaign.id)
    
    def test_finish_campaign_should_fail_with_no_verified_subscribers(self):
        campaign = Campaign.objects.create(title="Empty campaign", description="")
        not_veriefed_emails = [
            "john+04@doe.com",
            "john+05@doe.com",
            "john+06@doe.com",
        ]
        for email in not_veriefed_emails:
            self.campaign_manager.add_subscriber(
                campaign_id=campaign.id, 
                email=email, 
                subscriber_data=self.subscriber_data
            )
        with self.assertRaises(ValueError):
            self.campaign_manager.finish_campaign(campaign.id)

    def __get_verification_code(self, email, campaign_id):
        self.signer = Signer()
        code = {"email": email, "campaign_id": campaign_id}
        return self.signer.sign(json.dumps(code))

