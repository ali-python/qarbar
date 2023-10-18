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


# class UserSerializer(serializers.ModelSerializer):
#     agent_id = serializers.ReadOnlyField(source='agent.id')

#     class Meta:
#         model = User
#         fields = ['id','agent_id', 'username', 'first_name', 'last_name', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    agent_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'user_id', 'agent_id']
        extra_kwargs = {'password': {'write_only': True}}

    def get_user_id(self, obj):
        try:
            return obj.agent.user_id
        except Agent.DoesNotExist:
            return obj.id

    def get_agent_id(self, obj):
        try:
            agent_id = obj.agent.id
            return agent_id if agent_id is not None else None
        except Agent.DoesNotExist:
            return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['agent_id'] is None:
            del data['agent_id']
        elif data['agent_id'] is not None:
            del data['user_id']
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AgentUserUpdateSerializer(serializers.Serializer):
    agent_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    first_name = serializers.CharField(allow_blank=True, required=False)
    last_name = serializers.CharField(allow_blank=True, required=False)
    phone_number = serializers.CharField(allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    dob = serializers.DateField(required=False)
    city = serializers.CharField(allow_blank=True, required=False)
    country = serializers.CharField(allow_blank=True, required=False)

    def save(self, **kwargs):
        user_id = self.validated_data.get('user_id')
        agent_id = self.validated_data.get('agent_id')

        if not user_id and not agent_id:
            raise serializers.ValidationError("Either user_id or agent_id must be provided.")

        user = None
        user_profile = None

        if user_id:
            user = User.objects.get(pk=user_id)
            user_profile = user.userprofile
        elif agent_id:
            agent = Agent.objects.get(pk=agent_id)
            user = agent.user
            user_profile = user.userprofile

        if 'first_name' in self.validated_data:
            user.first_name = self.validated_data['first_name']

        if 'last_name' in self.validated_data:
            user.last_name = self.validated_data['last_name']

        if 'email' in self.validated_data:
            user.email = self.validated_data['email']

        user.save()

        if 'phone_number' in self.validated_data:
            user_profile.phone_number = self.validated_data['phone_number']

        if 'dob' in self.validated_data:
            user_profile.dob = self.validated_data['dob']

        if 'city' in self.validated_data:
            user_profile.city = self.validated_data['city']

        if 'country' in self.validated_data:
            user_profile.country = self.validated_data['country']

        user_profile.save()

        return user


class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(allow_null=True)
    whatsapp_num = serializers.CharField(allow_blank=True, required=False)
    phone_number = serializers.CharField(allow_blank=True, required=False)
    bio = serializers.CharField(allow_blank=True, required=False)
    nationality = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Agent
        fields = (
            'id', 'image', 'name', 'whatsapp_num', 'phone_number', 'landline_number', 'bio',
            'nationality', 'languages', 'areas', 'experience_since', 'user', 'views_count',
            'company_name', 'company_ntn', 'cnic', 'city', 'province', 'postal_code', 'user'
        )

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer().create(validated_data=user_data)
        
        agent = Agent.objects.create(user=user, **validated_data)
        return agent
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        # Update fields of the Agent model
        instance.image = validated_data.get('image', instance.image)
        print(instance.image)
        print("_____________________________________")
        instance.name = validated_data.get('name', instance.name)
        instance.whatsapp_num = validated_data.get('whatsapp_num', instance.whatsapp_num)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.landline_number = validated_data.get('landline_number', instance.landline_number)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.languages = validated_data.get('languages', instance.languages)
        instance.areas = validated_data.get('areas', instance.areas)
        instance.experience_since = validated_data.get('experience_since', instance.experience_since)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.company_ntn = validated_data.get('company_ntn', instance.company_ntn)
        instance.cnic = validated_data.get('cnic', instance.cnic)
        instance.city = validated_data.get('city', instance.city)
        instance.province = validated_data.get('province', instance.province)
        instance.postal_code = validated_data.get('postal_code', instance.postal_code)

        # Update fields of the User model
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        user.save()

        # Call the .save() method to save the changes to the Agent model
        instance.save()

        return instance

    
