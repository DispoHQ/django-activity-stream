import django
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.comments.signals import comment_was_posted

from actstream import action
from actstream.registry import register


def comment_action(sender, comment=None, target=None, **kwargs):
    if comment.user:
        action.send(comment.user, verb='commented', action_object=comment,
                    target=comment.content_object)
comment_was_posted.connect(comment_action)


@python_2_unicode_compatible
class Player(models.Model):
    state = models.IntegerField(default=0)

    def __str__(self):
        return '#%d' % self.pk


if django.VERSION <= (1, 7):
    register(Player)


@python_2_unicode_compatible
class Abstract(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Unregistered(Abstract):
    pass


if django.VERSION >= (1, 5):
    from django.contrib.admin import site
    from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

    class MyUserManager(BaseUserManager):
        def create_user(self, username, password=None):
            user = self.model(username=username)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, username, password):
            user = self.create_user(username, password=password)
            user.is_superuser = True
            user.save(using=self._db)
            return user

    class MyUser(AbstractBaseUser, PermissionsMixin):
        username = models.CharField(max_length=255, unique=True)
        is_active = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=True)

        objects = MyUserManager()

        USERNAME_FIELD = 'username'

        def get_full_name(self):
            return self.username
        get_short_name = get_full_name

    site.register(MyUser)

    if django.VERSION <= (1, 7):
        register(MyUser)