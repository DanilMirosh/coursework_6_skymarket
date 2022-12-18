from django.conf import settings
from django.db import models

from users.models import User


class Ad(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True)
    price = models.PositiveIntegerField()
    author = models.ForeignKey(User, related_name='ads', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ads/%Y/%m/%d/', null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ad = models.ForeignKey(Ad, related_name="comments", on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_at']

    def __str__(self):
        text = str(self.text)
        return text if len(text) <= 20 else text[:20] + "..."
