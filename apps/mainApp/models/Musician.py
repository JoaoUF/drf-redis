from django.db import models
from utils.model import Model
from django_extensions.db.models import ActivatorModel, TimeStampedModel


class Musician(ActivatorModel, TimeStampedModel, Model):
    firstName = models.CharField(
        db_column='first_name',
        max_length=50,
    )
    lastName = models.CharField(
        db_column='last_name',
        max_length=50,
    )
    instrument = models.CharField(
        db_column='instrument',
        max_length=100
    )

    def __str__(self):
        return self.firstName

    class Meta:
        db_table = 'MAE_MUSICIAN'
