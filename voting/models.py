from django.db import models

class Voter(models.Model):
    voter_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    has_voted = models.BooleanField(default=False)
    voted_party = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.voter_id})"
