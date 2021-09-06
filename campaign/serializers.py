from rest_framework import serializers
from campaign.models import Campaign, Subscriber

class CampaignSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'finished', 'winner']

class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'verified', 'subscriber_data']