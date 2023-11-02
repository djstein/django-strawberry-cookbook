from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def user_post_save(sender, instance, created, **kwargs):
    """Post save signal for user model."""
    # disable the handler during fixture loading
    if kwargs["raw"]:
        return

    if created and instance.username != "AnonymousUser":
        instance._assign_default_permissions()


@receiver(post_save, sender="authorization.Team")
def team_post_save(sender, instance, created, **kwargs):
    """Post save signal for team model."""
    if created and instance.id:
        instance._create_group()
        instance._create_admin_group()
