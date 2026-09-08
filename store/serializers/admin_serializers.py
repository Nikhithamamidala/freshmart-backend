from rest_framework import serializers
from django.contrib.auth.models import User

class AdminOrderStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[
        ('pending', 'Pending'), 
        ('processing', 'Processing'), 
        ('shipped', 'Shipped'), 
        ('delivered', 'Delivered'), 
        ('cancelled', 'Cancelled')
    ])

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active']