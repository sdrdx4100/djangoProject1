from django.contrib import admin
from .models import Constant

@admin.register(Constant)
class ConstantAdmin(admin.ModelAdmin):
    # models.pyの全項目をリスト表示
    list_display = (
        'id',
        'name',
        'name_key',
        'category',
        'category_key',
        'note',
        'created_at',
    )
    # 検索対象フィールド
    search_fields = ('name', 'name_key', 'category', 'category_key', 'note')
    # フィルタ
    list_filter = ('category', 'category_key', 'created_at')
