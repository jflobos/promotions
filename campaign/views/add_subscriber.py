from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from campaign.manager.campaign_manager import CampaignManager
from campaign.manager.exceptions import InvalidCampaignError, RepeatedEmailError

@api_view(['POST'])
@parser_classes([JSONParser])
def add_subscriber(request):
    try:
        campaign_manager = CampaignManager()
        email = request.data["email"]
        campaign_id = request.data["campaign_id"]
        subscriber_data = request.data["subscriber_data"]
        campaign_manager.add_subscriber(
            campaign_id=campaign_id, 
            email=email, 
            subscriber_data=subscriber_data
        )
        return reply_success()

    except InvalidCampaignError:
        return reply_invalid_campaign()
    
    except RepeatedEmailError:
        return reply_email_repeated()
    
    except:
        return reply_unknow_error()

def reply_success():
    response = Response({"status": "ok"}, status=status.HTTP_201_CREATED, content_type='json')
    return response

def reply_email_repeated():
    response = Response(
        {
            "status": "error",
            "error": "Email already registered"
        }, 
        status=status.HTTP_400_BAD_REQUEST, 
        content_type='json'
    )
    return response

def reply_invalid_campaign():
    response = Response(
        {
            "status": "error",
            "error": "Invalid Campaign"
        }, 
        status=status.HTTP_404_NOT_FOUND, 
        content_type='json'
    )
    return response

def reply_unknow_error():
    response = Response(
        {
            "status": "error",
            "error": "Unknow error"
        }, 
        status=status.HTTP_400_BAD_REQUEST, 
        content_type='json'
    )
    return response