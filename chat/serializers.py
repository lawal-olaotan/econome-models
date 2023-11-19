from rest_framework import serializers
from .models import UserTrials

class UserTrialSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserTrials
        fields = ["_id", "name", "icon", "domain", "ends", "starts", "postedBy", "isReminderset" ]

    