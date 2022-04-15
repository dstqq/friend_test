from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _

AUTH_USER_MODEL = getattr(settings, "AUTH_USER_MODEL", "auth.User")


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        max_length=100, verbose_name='Name', null=True, blank=True)
    username = models.CharField(
        unique=True, max_length=40, verbose_name='Usename')
    email = models.EmailField(
        unique=True, max_length=40, verbose_name='Email address')
    bio = models.TextField(null=True, blank=True, verbose_name='Bio')
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name='Date of Birth')
    friends = models.ManyToManyField(
        "CustomUser", blank=True, verbose_name="Friends")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_join = models.DateTimeField(
        default=timezone.now, verbose_name='Registration date')
    avatar = models.ImageField(null=True, default="avatar.svg")
 
    connect_telegram_form = models.SmallIntegerField(null=True, blank=True, verbose_name="Confirm telegram")
    is_connect_to_telegram = models.BooleanField(default=False, verbose_name="Connect telegram account")
    telegram_id = models.SmallIntegerField(
        null=True, blank=True, verbose_name="Telegram ID")
    telegram_confirm_code = models.SmallIntegerField(
        null=True, blank=True, verbose_name="Telegram confirm code")
        
    in_game_now = models.SmallIntegerField(
        default=0, verbose_name="Playing now or no")
    number_of_games = models.SmallIntegerField(
        default=0, verbose_name="number of games")
    last_game_date = models.DateTimeField(default=timezone.now, verbose_name='Last game date')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = 'users'
        verbose_name = 'user'


class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Friendship request"
        verbose_name_plural = "Friendship reauests"
        unique_together = ("from_user", "to_user")

    def accept(self):
        Friend.objects.create(from_user=self.from_user, to_user=self.to_user)
        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)
        self.delete()
        try:
            Friend_Request.objects.filter(
                from_user=self.to_user, to_user=self.from_user).delete()
        except:
            pass
        return True

    def reject(self):
        self.rejected = timezone.now()
        self.save()
        return True

    def cancel(self):
        self.delete()
        return True

    def viewed(self):
        self.viewed = timezone.now()
        self.save()
        return True


class Friend(models.Model):
    from_user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='from_user_friend', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='to_user_friend', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        return