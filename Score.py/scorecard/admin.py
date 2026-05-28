from django.contrib import admin
from .models import Team, Player, Match, MatchInnings, BattingScorecard, BowlingScorecard, BallByBall

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Match)
admin.site.register(MatchInnings)
admin.site.register(BattingScorecard)
admin.site.register(BowlingScorecard)
admin.site.register(BallByBall)

