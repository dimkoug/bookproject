from django.db import models
from django.utils.html import format_html, mark_safe


from core.models import Timestamped



class Author(Timestamped):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='authors/', null=True, blank=True)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'authors'
        verbose_name = 'author'
        verbose_name_plural = 'authors'

    def __str__(self):
        return self.name

    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''