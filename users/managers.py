from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models as django_models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


"""class FriendshipManager(django_models.Manager):


    def requsets(self, user):
        qs = Friend_Request.objects.select_related(
            "from_user", "to_user"
        ).filter(to_user=user)
        requests = list(qs)

        return requests

    def send_requests(self, user):
        qs = Friend_Request.objects.select_related(
            "from_user", "to_user"
        ).filter(from_user=user)
        requests = list(qs)

        return requests

    def add_friend(self, from_user, to_user, message=None):
        if from_user == to_user:
            raise ValidationError("Users cannot be friends with themselves")

        if self.are_friends(from_user, to_user):
            raise ValidationError("Users are already friends")

        if Friend_Request.objects.filter(
            from_user=from_user, to_user=to_user
        ).exists():
            raise ValidationError(
                "You already requested friendship from this user.")

        if Friend_Request.objects.filter(
            from_user=to_user, to_user=from_user
        ).exists():
            raise ValidationError(
                "This user already requested friendship from you.")

        if message is None:
            message = ""

        request, created = Friend_Request.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )

        if created is False:
            raise ValidationError("Friendship already requested")

        if message:
            request.message = message
            request.save()

        return request
"""

