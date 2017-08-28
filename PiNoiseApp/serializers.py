from rest_framework import serializers
from .models import Users,Posts,Votes

class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'
        