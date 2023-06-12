from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from . models import Agent, UserProfile

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='userprofile.phone_number', allow_null=True)
    dob = serializers.DateField(source='userprofile.dob', allow_null=True)
    city = serializers.CharField(source='userprofile.city', allow_null=True)
    country = serializers.CharField(source='userprofile.country', allow_null=True)
    address = serializers.CharField(source='userprofile.address', allow_null=True)
    is_agent = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'address',
            'dob',
            'city',
            'country',
            'is_staff',
            'is_agent'
        ]
        read_only_fields = ['id', 'username', 'is_staff', 'is_agent']

    def get_is_agent(self, obj):
        agent_user = Agent.objects.filter(user=obj).exists()
        return agent_user
    
class AuthTokenCustomSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            if '@' in username:
                e_user = User.objects.filter(email=username).first()
                username = e_user.username if e_user else username

            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=128, required=True)
    last_name = serializers.CharField(max_length=128, required=True)
    username = serializers.CharField(max_length=128, required=True)
    password = serializers.CharField(max_length=128, required=True)
    confirm_password = serializers.CharField(max_length=128, required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=20, required=True)
    dob = serializers.DateField(required=False)
    city = serializers.CharField(required=False)
    country = serializers.CharField(required=False)

    @staticmethod
    def validate_username(username):
        username = username.lower().strip()
        if ' ' in username:
            raise serializers.ValidationError('Invalid username.')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')

        return username

    @staticmethod
    def validate_password(password):
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(e)
        return password

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('Password is not matching')
        return attrs

    @staticmethod
    def validate_email(email):
        email = email.lower().strip()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        return email

    def save(self):
        user = User.objects.create(**{
            'email': self.validated_data.get('email'),
            'username': self.validated_data.get('username'),
            'first_name': self.validated_data.get('first_name'),
            'last_name': self.validated_data.get('last_name')
        })

        user.set_password(self.validated_data.get('password'))
        user.save()

        user.userprofile.phone_number = self.validated_data.get('phone_number')
        user.userprofile.save()
        return user


class UpdateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(allow_null=True, allow_blank=True)
    last_name = serializers.CharField(allow_null=True, allow_blank=True)
    phone_number = serializers.CharField(allow_null=True, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    dob = serializers.DateField(required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    country = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def save(self, **kwargs):
        user = self.context.get('request').user
        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        phone_number = self.validated_data.get('phone_number')
        email = self.validated_data.get('email')
        dob = self.validated_data.get('dob')
        city = self.validated_data.get('city')
        country = self.validated_data.get('country')

        if 'first_name' in self.data:
            user.first_name = first_name

        if 'last_name' in self.data:
            user.last_name = last_name

        if 'email' in self.data:
            user.email = email

        if 'phone_number' in self.data:
            user.userprofile = phone_number

        if 'dob' in self.data:
            user.userprofile = dob

        if 'city' in self.data:
            user.userprofile = city

        if 'country' in self.data:
            user.userprofile = country

        user.save()
        user.userprofile.save()

        return user
    
# class AgentSerializer(RegisterSerializer):
#     name = serializers.CharField(max_length=128, required=True)
#     bio = serializers.CharField(required=True)
#     nationality = serializers.CharField(max_length=50, required=True)
#     languages = serializers.CharField(max_length=200, required=True)
#     areas = serializers.CharField(max_length=200, required=True)
#     experience_since = serializers.DateField(required=True)

#     def create(self, validated_data):
#         user = super().create(validated_data)  # Call the parent create method to create the user

#         agent = Agent.objects.create(
#             user=user,
#             name=validated_data.get('name'),
#             bio=validated_data.get('bio'),
#             phone_number=validated_data.get('phone_number'),
#             email=validated_data.get('email'),
#             nationality=validated_data.get('nationality'),
#             languages=validated_data.get('languages'),
#             areas=validated_data.get('areas'),
#             experience_since=validated_data.get('experience_since')
#         )

#         return agent


class AgentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    email = serializers.CharField(source='user.email')
    phone_number = serializers.CharField(source='user.userprofile.phone_number')
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    name = serializers.CharField(max_length=128, required=True)
    bio = serializers.CharField(required=True)
    nationality = serializers.CharField(max_length=50, required=True)
    languages = serializers.CharField(max_length=200, required=True)
    areas = serializers.CharField(max_length=200, required=True)
    experience_since = serializers.DateField(required=True)

    def create(self, validated_data):
        user_data = {
            'username': validated_data['user']['username'],
            'password': validated_data['user']['password'],
            'email': validated_data['user']['email'],
            'first_name': '',
            'last_name': '',
        }
        user_profile_data = {
            'phone_number': validated_data['user']['userprofile']['phone_number'],
        }
        agent_data = {
            'name': validated_data['name'],
            'bio': validated_data['bio'],
            'nationality': validated_data['nationality'],
            'languages': validated_data['languages'],
            'areas': validated_data['areas'],
            'experience_since': validated_data['experience_since'],
        }

        user = User.objects.create(**user_data)
        UserProfile.objects.create(user=user, **user_profile_data)
        agent = Agent.objects.create(user=user, **agent_data)

        return agent

    class Meta:
        model = Agent
        fields = (
            'username', 'password', 'email', 'phone_number',
            'first_name', 'last_name', 'name', 'bio',
            'nationality', 'languages', 'areas', 'experience_since'
        )













