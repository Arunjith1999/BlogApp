from rest_framework import serializers
from .models import Blog,Comment,Customuser

class BlogSerializer(serializers.ModelSerializer):
    user_image = serializers.SerializerMethodField()  # Create a custom field for user image
    username    = serializers.SerializerMethodField() # Create a custom field for username
    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'user_image', 'username']

    def get_user_image(self, obj):          #used to get related fields values
        if obj.user and obj.user.image:
            return obj.user.image.url
        else:
            return None
        
    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return None


class CommentSerializer(serializers.ModelSerializer):# seralizer for Comment table
    username    = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['content', 'username']            #serailizing specific fields

    def get_username(self, obj):                    #get username which is a related  field
        if obj.user:
            return obj.user.username
        else:
            return None

class UserSerializer(serializers.ModelSerializer):# seralizer for Customuser table
    class Meta:
        model = Customuser                             
        fields ='__all__'                          #serilaizing all the fields