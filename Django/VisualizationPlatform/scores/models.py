from django.db import models

# Create your models here.
class Score(models.Model):
    year = models.IntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    # 添加九种科目的字段
    language = models.DecimalField(max_digits=5, decimal_places=2)
    mathematics = models.DecimalField(max_digits=5, decimal_places=2)
    english = models.DecimalField(max_digits=5, decimal_places=2)
    chemistry = models.DecimalField(max_digits=5, decimal_places=2)
    physics = models.DecimalField(max_digits=5, decimal_places=2)
    biology = models.DecimalField(max_digits=5, decimal_places=2)
    geography = models.DecimalField(max_digits=5, decimal_places=2)
    politics = models.DecimalField(max_digits=5, decimal_places=2)
    history = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.year}年 成绩"