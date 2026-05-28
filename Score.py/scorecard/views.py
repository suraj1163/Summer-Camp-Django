from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Team, Player, Match, MatchInnings, BattingScorecard, BowlingScorecard, BallByBall
from .serializers import (
    TeamSerializer, TeamDetailSerializer, PlayerSerializer, MatchSerializer,
    MatchInningsSerializer, BattingScorecardSerializer, BowlingScorecardSerializer,
    BallByBallSerializer, MatchFullScorecardSerializer
)

class IsScorerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authenticated scorers to edit/create, 
    but anyone can view.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    permission_classes = [IsScorerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsScorerOrReadOnly]
    filterset_fields = ['team']

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [IsScorerOrReadOnly]

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def scorecard(self, request, pk=None):
        """
        Retrieves the complete deep nested scorecard for the match.
        """
        match = self.get_object()
        serializer = MatchFullScorecardSerializer(match)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def start_innings(self, request, pk=None):
        """
        Initializes a match innings.
        Expected POST parameters:
        - innings_number: 1 or 2
        - batting_team: Team ID
        """
        match = self.get_object()
        innings_number = request.data.get('innings_number')
        batting_team_id = request.data.get('batting_team')

        if not innings_number or not batting_team_id:
            return Response(
                {"error": "Please provide both 'innings_number' and 'batting_team' id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            innings_number = int(innings_number)
            batting_team = Team.objects.get(id=batting_team_id)
        except (ValueError, Team.DoesNotExist):
            return Response(
                {"error": "Invalid innings_number or batting_team id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify team participates in match
        if batting_team != match.team_a and batting_team != match.team_b:
            return Response(
                {"error": "This team is not participating in this match."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Determine bowling team
        bowling_team = match.team_b if batting_team == match.team_a else match.team_a

        # Create or fetch Innings
        innings, created = MatchInnings.objects.get_or_create(
            match=match,
            innings_number=innings_number,
            defaults={
                'batting_team': batting_team,
                'bowling_team': bowling_team
            }
        )

        if not created:
            return Response(
                {"message": f"Innings {innings_number} has already been started.", "innings": MatchInningsSerializer(innings).data},
                status=status.HTTP_200_OK
            )

        # Automatically update match status to Live
        if match.status == 'Scheduled':
            match.status = 'Live'
            match.save()

        return Response({
            "message": f"Innings {innings_number} started successfully.",
            "innings": MatchInningsSerializer(innings).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def record_ball(self, request, pk=None):
        """
        Records a single delivery event (BallByBall).
        Automatically recalculates scorecards and returns the updated innings summary.
        Expected POST parameters:
        - innings_number: 1 or 2
        - over_number: integer (0-indexed)
        - ball_number: integer (1-6)
        - batsman: Player ID (Striker)
        - bowler: Player ID
        - non_striker: Player ID (Non-Striker)
        - runs_batsman: integer (default 0)
        - runs_extras: integer (default 0)
        - extra_type: 'None'/'Wide'/'No Ball'/'Leg Bye'/'Bye' (default 'None')
        - wicket: boolean (default False)
        - wicket_type: 'None'/'Bowled'/'Caught'/'LBW'/'Run Out'/'Stumped'/'Retired Hurt'/'Hit Wicket' (default 'None')
        - dismissed_player: Player ID (optional)
        - fielder: Player ID (optional)
        - commentary: text (optional)
        """
        match = self.get_object()
        innings_number = request.data.get('innings_number')

        if not innings_number:
            return Response({"error": "Please provide 'innings_number'."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            innings = MatchInnings.objects.get(match=match, innings_number=innings_number)
        except MatchInnings.DoesNotExist:
            return Response({"error": f"Innings {innings_number} has not been started yet. Call start_innings first."}, status=status.HTTP_404_NOT_FOUND)

        # Build data dictionary and validate serializer
        data = request.data.copy()
        data['innings'] = innings.id

        # Defaults
        if 'runs_batsman' not in data: data['runs_batsman'] = 0
        if 'runs_extras' not in data: data['runs_extras'] = 0
        if 'extra_type' not in data: data['extra_type'] = 'None'
        if 'wicket' not in data: data['wicket'] = False
        if 'wicket_type' not in data: data['wicket_type'] = 'None'

        serializer = BallByBallSerializer(data=data)
        if serializer.is_valid():
            # Saving will automatically trigger models.py recalculate_innings_scorecard!
            delivery = serializer.save()

            # Refresh innings from DB to get the freshly recalculated scores
            innings.refresh_from_db()
            innings_data = MatchInningsSerializer(innings).data

            return Response({
                "message": "Ball recorded successfully.",
                "delivery": serializer.data,
                "innings_summary": {
                    "total_runs": innings.total_runs,
                    "total_wickets": innings.total_wickets,
                    "overs": innings.overs,
                    "run_rate": innings.run_rate
                }
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MatchInningsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MatchInnings.objects.all()
    serializer_class = MatchInningsSerializer
    permission_classes = [permissions.AllowAny]

class BattingScorecardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BattingScorecard.objects.all()
    serializer_class = BattingScorecardSerializer
    permission_classes = [permissions.AllowAny]

class BowlingScorecardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BowlingScorecard.objects.all()
    serializer_class = BowlingScorecardSerializer
    permission_classes = [permissions.AllowAny]

class BallByBallViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BallByBall.objects.all()
    serializer_class = BallByBallSerializer
    permission_classes = [permissions.AllowAny]
