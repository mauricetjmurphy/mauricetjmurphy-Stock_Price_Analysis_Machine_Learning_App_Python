from django.contrib.auth.models import User, Group
from .models import Predictions
from rest_framework import serializers


class PredictionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Predictions
        fields = '__all__'
