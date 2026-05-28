from rest_framework import serializers
from .models import Team, Player, Match, MatchInnings, BattingScorecard, BowlingScorecard, BallByBall

class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_short_name = serializers.CharField(source='team.short_name', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Player
        fields = ('id', 'team', 'team_name', 'team_short_name', 'first_name', 'last_name', 'full_name', 'role', 'batting_style', 'bowling_style')

class TeamSerializer(serializers.ModelSerializer):
    player_count = serializers.IntegerField(source='players.count', read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'short_name', 'player_count')

class TeamDetailSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'short_name', 'players')

class MatchSerializer(serializers.ModelSerializer):
    team_a_name = serializers.CharField(source='team_a.name', read_only=True)
    team_b_name = serializers.CharField(source='team_b.name', read_only=True)
    team_a_short = serializers.CharField(source='team_a.short_name', read_only=True)
    team_b_short = serializers.CharField(source='team_b.short_name', read_only=True)
    winner_name = serializers.CharField(source='winner.name', read_only=True)

    class Meta:
        model = Match
        fields = (
            'id', 'title', 'team_a', 'team_b', 'team_a_name', 'team_b_name', 
            'team_a_short', 'team_b_short', 'match_type', 'overs_limit', 
            'venue', 'date', 'toss_winner', 'toss_decision', 'status', 
            'winner', 'result_margin', 'created_at'
        )

class BattingScorecardSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    dismissed_by_name = serializers.CharField(source='dismissed_by.full_name', read_only=True)
    fielder_name = serializers.CharField(source='fielder.full_name', read_only=True)
    strike_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = BattingScorecard
        fields = (
            'id', 'player', 'player_name', 'runs', 'balls_faced', 'fours', 'sixes', 
            'dismissal_status', 'dismissed_by', 'dismissed_by_name', 
            'fielder', 'fielder_name', 'strike_rate'
        )

class BowlingScorecardSerializer(serializers.ModelSerializer):
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    overs = serializers.CharField(read_only=True)
    economy_rate = serializers.FloatField(read_only=True)

    class Meta:
        model = BowlingScorecard
        fields = (
            'id', 'player', 'player_name', 'balls_bowled', 'overs', 
            'runs_conceded', 'wickets', 'maidens', 'wides_bowled', 
            'noballs_bowled', 'economy_rate'
        )

class BallByBallSerializer(serializers.ModelSerializer):
    batsman_name = serializers.CharField(source='batsman.full_name', read_only=True)
    bowler_name = serializers.CharField(source='bowler.full_name', read_only=True)
    non_striker_name = serializers.CharField(source='non_striker.full_name', read_only=True)
    dismissed_player_name = serializers.CharField(source='dismissed_player.full_name', read_only=True)
    fielder_name = serializers.CharField(source='fielder.full_name', read_only=True)

    class Meta:
        model = BallByBall
        fields = (
            'id', 'innings', 'over_number', 'ball_number', 'batsman', 'batsman_name',
            'bowler', 'bowler_name', 'non_striker', 'non_striker_name',
            'runs_batsman', 'runs_extras', 'extra_type', 'wicket', 
            'wicket_type', 'dismissed_player', 'dismissed_player_name', 
            'fielder', 'fielder_name', 'commentary', 'timestamp'
        )

class MatchInningsSerializer(serializers.ModelSerializer):
    batting_team_name = serializers.CharField(source='batting_team.name', read_only=True)
    bowling_team_name = serializers.CharField(source='bowling_team.name', read_only=True)
    batting_team_short = serializers.CharField(source='batting_team.short_name', read_only=True)
    bowling_team_short = serializers.CharField(source='bowling_team.short_name', read_only=True)
    overs = serializers.CharField(read_only=True)
    run_rate = serializers.FloatField(read_only=True)
    
    # Nested stats lists
    batsmen_stats = BattingScorecardSerializer(many=True, read_only=True)
    bowlers_stats = BowlingScorecardSerializer(many=True, read_only=True)
    deliveries = BallByBallSerializer(many=True, read_only=True)

    class Meta:
        model = MatchInnings
        fields = (
            'id', 'innings_number', 'batting_team', 'batting_team_name', 'batting_team_short',
            'bowling_team', 'bowling_team_name', 'bowling_team_short', 'total_runs', 
            'total_wickets', 'total_balls', 'overs', 'run_rate', 'is_completed', 
            'batsmen_stats', 'bowlers_stats', 'deliveries'
        )

class MatchFullScorecardSerializer(serializers.ModelSerializer):
    team_a_name = serializers.CharField(source='team_a.name', read_only=True)
    team_b_name = serializers.CharField(source='team_b.name', read_only=True)
    team_a_short = serializers.CharField(source='team_a.short_name', read_only=True)
    team_b_short = serializers.CharField(source='team_b.short_name', read_only=True)
    winner_name = serializers.CharField(source='winner.name', read_only=True)
    
    # Deep nested innings
    innings = MatchInningsSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = (
            'id', 'title', 'team_a', 'team_b', 'team_a_name', 'team_b_name', 
            'team_a_short', 'team_b_short', 'match_type', 'overs_limit', 
            'venue', 'date', 'toss_winner', 'toss_decision', 'status', 
            'winner', 'winner_name', 'result_margin', 'innings', 'created_at'
        )
