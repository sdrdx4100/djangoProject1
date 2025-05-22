from django.contrib import admin
from .models import Information
from markdownx.admin import MarkdownxModelAdmin

@admin.register(Information)
class InformationAdmin(MarkdownxModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)