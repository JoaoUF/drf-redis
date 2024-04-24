from django.db import models
from utils.model import Model
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from .Musician import Musician


class Album(ActivatorModel, TimeStampedModel, Model):
    artist = models.ForeignKey(
        Musician,
        on_delete=models.CASCADE,
        db_column='artist',
    )
    name = models.CharField(
        max_length=100,
        db_column='name',
    )
    releaseDate = models.DateField(
        db_column='release_date',
    )
    numStart = models.IntegerField(
        db_column='num_start',
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'MAE_ALBUM'
