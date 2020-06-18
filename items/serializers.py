from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Item, Rating


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields=['username', 'password', 'id']


    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        read_only_fields = ['item_rating']
        

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'



class ItemRatingSerializer(serializers.Serializer):
    product = ItemSerializer()
    rating = RatingSerializer(many=True)

    
    
    


    