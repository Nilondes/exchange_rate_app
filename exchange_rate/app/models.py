from django.db import models
from django.contrib.auth.models import User


class ExchangeRateResponseManager(models.Manager):
    def for_user(self, user):
        return self.get_queryset().filter(user=user)


class ExchangeRateResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    response = models.JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = ExchangeRateResponseManager()

    def __str__(self):
        return f"{self.user} - {self.timestamp} - {self.response}"
