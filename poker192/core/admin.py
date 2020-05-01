from django.contrib import admin
from core.models import Game, Card, Hand, Board, Deck
# Register your models here.

admin.site.register(Game)
admin.site.register(Card)
admin.site.register(Hand)
admin.site.register(Board)
admin.site.register(Deck)