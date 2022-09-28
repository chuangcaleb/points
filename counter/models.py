from django.db import models

# Create your models here.


class PointsRecord(models.Model):

    group = models.CharField(max_length=200, primary_key=True)
    points = models.IntegerField(default=0, null=False)

    @property
    def uppercase_group(self):
        return self.group.upper()

    def __str__(self):
        return self.uppercase_group

    class Meta:
        indexes = [
            models.Index(fields=['group'], name='group_idx'),
        ]
