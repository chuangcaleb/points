from django.db import models
from django.template.defaultfilters import slugify
import html

# Create your models here.


class Event(models.Model):

    name = models.CharField(max_length=200, primary_key=True)
    slug = models.SlugField('slug', max_length=64)
    bg_url = models.CharField(max_length=500, null=True, blank=True)
    font = models.CharField(max_length=100, null=True, blank=True)
    font_link = models.CharField(max_length=300, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    default_card_color = models.CharField(max_length=20, null=True, blank=True)
    heading_size = models.CharField(max_length=5, null=True, blank=True)
    points_size = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        def sanitize_css(string):
            temp_font = html.escape(string)
            return temp_font.replace("&#x27;", "'")

        # Sanitize font css
        if self.font:
            self.font = sanitize_css(self.font)

        # Only generates the slug on first creation
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Group(models.Model):

    name = models.CharField(max_length=200, primary_key=True)
    points = models.IntegerField(default=0, null=False)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="event_group"
    )
    slug = models.SlugField('slug', max_length=64, null=True)
    color = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'], name='group_name_idx'),
        ]

    @property
    def uppercase_name(self):
        return self.name.upper()

    def __str__(self):
        return f"{self.event}: {self.uppercase_name}"

    def save(self, *args, **kwargs):

        # Slugify
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Group, self).save(*args, **kwargs)


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
