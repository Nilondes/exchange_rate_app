from django.db import models
from django.contrib.auth.models import User


class ExchangeRateResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    response = models.JSONField()

    def __str__(self):
        return f"{self.user} - {self.response}"
