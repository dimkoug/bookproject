from django.db import models
from django.utils.html import format_html, mark_safe


from core.models import Timestamped


class Publisher(Timestamped):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    authors = models.ManyToManyField('authors.Author', through='PublishingContract', blank=True)
    image = models.ImageField(upload_to='publishers/', null=True, blank=True)
    profile = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'publishers'
        verbose_name = 'publisher'
        verbose_name_plural = 'publishers'

    def __str__(self):
        return self.name

    def get_thumb(self):
        if self.image:
            return format_html("<img src='{}' width='100' height='auto'>",
                               self.image.url)
        return ''

class PublishingContract(models.Model):
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    contract_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)  # ⬅️ new field!

    class Meta:
        unique_together = ('author', 'publisher')

    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return not self.expiry_date or self.expiry_date >= today

    def __str__(self):
        return f"{self.author} with {self.publisher}"