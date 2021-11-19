from django.db import models

class Predictions(models.Model):
    predictions = models.IntegerField()

    def __str__(self):
        return self.predictions
