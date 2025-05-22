from django.db import models
from markdownx.models import MarkdownxField

class Information(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = MarkdownxField(help_text="Markdown形式で入力してください")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delete_flg = models.BooleanField(default=False, verbose_name="削除フラグ")

    def __str__(self):
        return self.title
    