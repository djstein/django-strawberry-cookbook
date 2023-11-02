from uuid import uuid4

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm

DEFAULT_USER_TIED_PERMISSION_CODENAMES = [
    "authorization.change_user",
]
DEFAULT_GLOBAL_PERMISSION_CODENAMES = [
    "authorization.add_team",
]


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    def _assign_default_permissions(self):
        # here we are tying permissions for this user to the user itself
        for permission_codename in DEFAULT_USER_TIED_PERMISSION_CODENAMES:
            assign_perm(permission_codename, self, self)
        # here we are tying global permissions to this user
        for permission_codename in DEFAULT_GLOBAL_PERMISSION_CODENAMES:
            assign_perm(permission_codename, self)


class Team(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created At"),
        help_text=_("When this team was created"),
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated At"),
        help_text=_("When this team was updated"),
        auto_now=True,
    )
    name = models.CharField(
        verbose_name=_("Name"),
        help_text=_("The name of this organization"),
        max_length=255,
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        help_text=_("The slug of this organization"),
        max_length=255,
    )
    created_by = models.ForeignKey(
        to=User,
        verbose_name=_("Created By"),
        help_text=_("The user that created this team"),
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        # add_modelname, change_modelname, delete_modelname, and view_modelname
        # are created by default
        permissions = (
            ("add_user_to_team", "Add user to team"),
            ("remove_user_from_team", "Add user to team"),
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def _create_admin_group(self):
        # create the team's admin group
        admin_group = Group.objects.create(
            name=self.name + " Admin",
        )
        # add the team permissions to the admin group
        assign_perm("authorization.change_team", admin_group, self)
        assign_perm("authorization.delete_team", admin_group, self)
        assign_perm("authorization.add_user_to_team", admin_group, self)
        assign_perm("authorization.remove_user_from_team", admin_group, self)

        # add the created_by user to the admin group
        self.created_by.groups.add(admin_group)

    def _create_group(self):
        # create the team's group
        group = Group.objects.create(
            name=self.name,
        )
        # add the team permissions to the group
        assign_perm("authorization.view_team", group, self)

        # add the created_by user to the group
        self.created_by.groups.add(group)
