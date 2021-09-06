from django.core.validators import EmailValidator
from campaign.models import Campaign, Subscriber

class CampaignManager:
    """Business logic implementation"""

    def add_subscriber(self, campaign_id, email, subscriber_data) -> Subscriber:
        self.__check_valid_inputs(campaign_id=campaign_id, email=email)
        subscriber = Subscriber.objects.create(
            campaign_id=campaign_id, 
            email=email, 
            user_data=subscriber_data
        )
        return subscriber

    def __check_valid_inputs(self, campaign_id, email):
        self.__check_campaign(campaign_id=campaign_id)
        self.__check_valid_email(email=email)
        self.__check_repeteated_email(campaign_id=campaign_id,email=email)
    
    def __check_campaign(self, campaign_id):
        if not Campaign.objects.filter(id=campaign_id).exists():
            raise ValueError("Invalid Campaign")

    def __check_valid_email(self, email):
        validator = EmailValidator()
        validator(email)
    
    def __check_repeteated_email(self, campaign_id, email) -> bool:
        if Subscriber.objects.filter(campaign_id=campaign_id, email=email).exists():
            raise ValueError("Email already registered") 

