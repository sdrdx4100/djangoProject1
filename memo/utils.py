# memo/utils.py
from django.core.cache import cache
from constant_master.models import Constant

def get_cached_constants(category, timeout=3600):
    """キャッシュを利用して定数を取得"""
    cache_key = f"constants_{category}"
    constants = cache.get(cache_key)

    if constants is None:
        constants = list(Constant.objects.filter(category=category))
        cache.set(cache_key, constants, timeout)

    return constants