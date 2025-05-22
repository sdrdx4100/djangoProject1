from django.db import models

class Constant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('定数文言', max_length=255)
    name_key = models.CharField('定数キー', null=True, max_length=255)
    category = models.CharField('定数分類', max_length=100)
    category_key = models.CharField('定数分類キー', null=True, max_length=255)
    note = models.TextField('備考', blank=True, null=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)

    # class Metaでdb_tableを指定しない場合、テーブル名は「constant_master_constant」になります
    def __str__(self):
        return f"{self.category}: {self.name}"

    class Meta:
        verbose_name = '定数'
        verbose_name_plural = '定数'
        ordering = ['category', 'name']
        db_table = 'constant_master'

