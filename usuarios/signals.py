from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model


@receiver(post_migrate)
def create_superuser_if_not_exists(sender, **kwargs):
    User = get_user_model()
    from django.conf import settings

    if settings.configured and settings.DEBUG:
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username="aluon",
                email="aluon.aluoni@gmail.com",
                password="123456"
            )
            print("Superusuário criado com sucesso.")
