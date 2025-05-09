from django.contrib import admin
from .models import Memo, Tag

admin.site.register(Memo)
admin.site.register(Tag)
