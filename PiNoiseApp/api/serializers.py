from rest_framework import serializers
from rest_framework.serializers import CharField
from ..models import User, Users, Posts, Votes, Category, ReplyPost, ReplytoReply, Reports
from django.contrib.auth import get_user_model

user = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = user
        fields = ["username","password","first_name","last_name","email"]
        extra_kwargs = {"password":{"write_only":True}
        }
        
    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        email = validated_data["email"]
        user_obj = User(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLogInSerializer(serializers.ModelSerializer):
    username = CharField(required = False, allow_blank = True)
    token = CharField(allow_blank = True, read_only = True)
    class Meta:
        model = user
        fields = ["username","password","token"]
        extra_kwargs = {"password":{"write_only":True}
        }

    def validate(self, data):
        username = data.get["username",None]
        password = data.get["password", None]
        user = User.objects.get(username = username)
        if user:
            if not user.check_password(password):
                raise ValidationError("Incorrect Credentials!")
        return data

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
        
class PostsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = '__all__'
        
class VotesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Votes
        fields = '__all__'
        
class ReplyPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplyPost
        fields = '__all__'
        
class ReplytoReplySerializer(serializers.ModelSerializer):

    class Meta:
        model = ReplytoReply
        fields = '__all__'
        
class ReportsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        fields = '__all__'
        