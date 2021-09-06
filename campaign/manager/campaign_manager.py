from campaign.manager.subscriber_helpers import create_verification_code, validate_subscriber
from campaign.models import Campaign, Subscriber

class CampaignManager:
    """Business logic implementation"""

    def add_subscriber(self, campaign_id, email, subscriber_data) -> Subscriber:
        validate_subscriber(campaign_id=campaign_id, email=email)
        subscriber = Subscriber.objects.create(
            campaign_id=campaign_id, 
            email=email, 
            user_data=subscriber_data,
            verification_code=create_verification_code(email=email, campaign_id=campaign_id)
        )
        return subscriber

    def verify_email(self, verification_code) -> bool:
        subscriber = Subscriber.objects.filter(verification_code=verification_code).first()
        if subscriber is None:
            raise ValueError("Invalid token")
        if subscriber.verified:
            raise ValueError("User already validated")
        subscriber.verified = True
        subscriber.save()
        return True

