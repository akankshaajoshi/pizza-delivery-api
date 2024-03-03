from .models import User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

class UserCreationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phonenumber = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phonenumber', 'password']

    def validate(self, attrs):
        username_exists = User.objects.filter(username=attrs.get('username')).exists()
        email_exists = User.objects.filter(email=attrs.get('email')).exists()
        phonenumber_exists = User.objects.filter(phonenumber=attrs.get('phonenumber')).exists()
        

        if username_exists:
            raise serializers.ValidationError(detail = "User with this username exists")
        
        if email_exists:
            raise serializers.ValidationError(detail = "User with this email exists")
        
        if phonenumber_exists:
            raise serializers.ValidationError(detail = "User with this phonenumber exists")
        
        return super().validate(attrs)

    def create(self, validated_data):
        
        user = User.objects.create(
            username=validated_data['username'],
            email = validated_data['email'],
            phonenumber = validated_data['phonenumber']
        )

        user.set_password(validated_data['password'])

        user.save()

        return user