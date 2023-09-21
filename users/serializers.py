from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth.models import User
from .models import Agent

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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'dob', 'city', 'country', 'address')


class UserSerializer(serializers.ModelSerializer):
    agent_id = serializers.ReadOnlyField(source='agent.id')

    class Meta:
        model = User
        fields = ['id','agent_id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True)
    # properties = PropertySerializer(many=True, read_only=True)
    class Meta:
        model = Agent
        fields = (
            'id','name', 'whatsapp_num', 'phone_number', 'bio',
            'nationality', 'languages', 'areas', 'experience_since', 'user', 'views_count',
            'company_name','company_ntn','cnic','city','province','postal_code'
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(validated_data=user_data)
        
        agent = Agent.objects.create(user=user, **validated_data)
        return agent









