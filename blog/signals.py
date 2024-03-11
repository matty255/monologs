from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Category


@receiver(post_save, sender=Category)
def clear_category_cache(sender, instance, **kwargs):
    cache_key = f"user_{instance.author.pk}_category"
    cache.delete(cache_key)


@receiver(post_delete, sender=Category)
def clear_category_cache_on_delete(sender, instance, **kwargs):
    cache_key = f"user_{instance.author.pk}_category"
    cache.delete(cache_key)
