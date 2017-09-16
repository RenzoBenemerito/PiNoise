from rest_framework import serializers
from .models import Users,Posts,Votes,Category,ReplyPost,ReplytoReply,Reports


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'
        
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
        