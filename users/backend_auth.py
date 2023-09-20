from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Check if the provided username is an email
        if UserModel.objects.filter(email=username).exists():
            user = UserModel.objects.get(email=username)
            # Check the password against the user
            if user.check_password(password):
                return user

        # If not, fall back to username-based authentication
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return user

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
