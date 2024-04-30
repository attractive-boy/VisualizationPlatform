from django.db import models

# Create your models here.
class Score(models.Model):
    year = models.IntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    subject = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.year}年 {self.subject} 成绩"