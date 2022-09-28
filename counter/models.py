from django.db import models

# Create your models here.


class Group(models.Model):

    name = models.CharField(max_length=200, primary_key=True)
    points = models.IntegerField(default=0, null=False)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='group_name_idx'),
        ]

    @property
    def uppercase_name(self):
        return self.name.upper()

    def __str__(self):
        return self.uppercase_name


# class PointsRecord(models.Model):

#     group = models.OneToOneField(
#         Group, on_delete=models.CASCADE, related_name="points_group", primary_key=True
#     )
#     # group = models.CharField(max_length=200, primary_key=True)
#     points = models.IntegerField(default=0, null=False)

#     def __str__(self):
#         return f"{self.group}: {self.points} points"


class PointsHistory(models.Model):
    # group = models.CharField(max_length=200, primary_key=True)
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="history_group"
    )
    offset = models.IntegerField(default=0, null=False)

    class Meta:
        verbose_name_plural = "Points histories"

    def __str__(self):
        return f"{self.group}: {self.offset} points"
