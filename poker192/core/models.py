from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    player = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING)
    numWins = models.BigIntegerField
    player_stack = models.BigIntegerField
    bot_stack = models.BigIntegerField
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.player