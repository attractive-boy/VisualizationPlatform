from django.db import models

class ScoreStatistics(models.Model):
    year = models.IntegerField()
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    data_count = models.IntegerField()
    total_score = models.DecimalField(max_digits=65, decimal_places=2)
    pass_count = models.IntegerField()
    language_score = models.DecimalField(max_digits=65, decimal_places=2)
    mathematics_score = models.DecimalField(max_digits=65, decimal_places=2)
    english_score = models.DecimalField(max_digits=65, decimal_places=2)
    chemistry_score = models.DecimalField(max_digits=65, decimal_places=2)
    physics_score = models.DecimalField(max_digits=65, decimal_places=2)
    biology_score = models.DecimalField(max_digits=65, decimal_places=2)
    geography_score = models.DecimalField(max_digits=65, decimal_places=2)
    politics_score = models.DecimalField(max_digits=65, decimal_places=2)
    history_score = models.DecimalField(max_digits=65, decimal_places=2)

    def __str__(self):
        return f"{self.year} - {self.province} - {self.city}"

    class Meta:
        unique_together = ('year', 'province', 'city')
