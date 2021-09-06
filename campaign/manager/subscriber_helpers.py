from campaign.manager.exceptions import InvalidCampaignError, RepeatedEmailError
import json
from django.core.signing import Signer
from django.core.validators import EmailValidator
from campaign.models import Campaign, Subscriber

def validate_subscriber(campaign_id, email):
    check_campaign(campaign_id=campaign_id)
    check_valid_email(email=email)
    check_repeteated_email(campaign_id=campaign_id,email=email)

def check_campaign(campaign_id):
    if not Campaign.objects.filter(id=campaign_id).exists():
        raise InvalidCampaignError("Invalid Campaign")

def check_valid_email(email):
    validator = EmailValidator()
    validator(email)
    
def check_repeteated_email(campaign_id, email) -> bool:
    if Subscriber.objects.filter(campaign_id=campaign_id, email=email).exists():
        raise RepeatedEmailError("Email already registered") 

def create_verification_code(email, campaign_id) -> str:
    data = { "email": email, "campaign_id": campaign_id }
    signer = Signer()
    return signer.sign_object(data)