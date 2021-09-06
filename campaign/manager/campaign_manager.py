from random import randint
from campaign.manager.subscriber_helpers import check_campaign, create_verification_code, validate_subscriber
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

    def finish_campaign(self, campaign_id):
       check_campaign(campaign_id)
       verified_subscribers = Subscriber.objects.filter(campaign_id=campaign_id, verified=True).all()
       if len(verified_subscribers) == 0:
           raise ValueError("Cannot finish campaign due to insuficent verified users")
       winner = self.__get_ramdom_from_array(verified_subscribers)
       campaign = Campaign.objects.get(pk=campaign_id)
       campaign.winner = winner.id
       campaign.finished = True
       campaign.save()

    def __get_ramdom_from_array(self, array):
        index = randint(0, len(array)-1)
        return array[index]

       

