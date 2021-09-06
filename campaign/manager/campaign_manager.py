from django.core.validators import EmailValidator
from campaign.models import Campaign, Subscriber

class CampaignManager:
    """Business logic implementation"""

    def add_subscriber(self, campaign_id, email, subscriber_data) -> Subscriber:
        if not self.__check_campaign(campaign_id=campaign_id):
            raise ValueError("Invalid Campaign")
        if not self.__check_valid_email(email=email):
            raise ValueError("Invalid email passed")
        subscriber = Subscriber.objects.create(
            campaign_id=campaign_id, 
            email=email, 
            user_data=subscriber_data
        )
        return subscriber
    
    def __check_campaign(self, campaign_id) -> bool:
        return Campaign.objects.filter(id=campaign_id).exists()

    def __check_valid_email(self, email) -> bool:
        validator = EmailValidator()
        result = validator(email)
        if result is None:
            return True
        return False
