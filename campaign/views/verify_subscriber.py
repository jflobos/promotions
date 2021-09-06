from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from campaign.manager.campaign_manager import CampaignManager

@api_view(['GET'])
def verify_subscriber(request):
    try:
        data = dict(request.GET)
        code = data['code'][0]
        campaign_manager = CampaignManager()
        campaign_manager.verify_email(verification_code=code)
        return Response(
            {
            "status": "success",
            "error": "Email verified"
            }, 
            status=status.HTTP_200_OK, 
            content_type='json'
        )

    except:
        return Response(
            {
            "status": "error",
            "error": "Bad request"
            }, 
            status=status.HTTP_400_BAD_REQUEST, 
            content_type='json'
        )

