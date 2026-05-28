from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TeamViewSet, PlayerViewSet, MatchViewSet, MatchInningsViewSet,
    BattingScorecardViewSet, BowlingScorecardViewSet, BallByBallViewSet
)

router = DefaultRouter()
router.register(r'teams', TeamViewSet)
router.register(r'players', PlayerViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'innings', MatchInningsViewSet)
router.register(r'batting-scorecards', BattingScorecardViewSet)
router.register(r'bowling-scorecards', BowlingScorecardViewSet)
router.register(r'deliveries', BallByBallViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
