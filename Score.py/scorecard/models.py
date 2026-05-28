from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True, help_text="e.g., IND, AUS, ENG")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.short_name})"

class Player(models.Model):
    ROLE_CHOICES = (
        ('Batsman', 'Batsman'),
        ('Bowler', 'Bowler'),
        ('All-Rounder', 'All-Rounder'),
        ('Wicket-Keeper', 'Wicket-Keeper'),
    )
    BATTING_STYLE_CHOICES = (
        ('Right-Hand', 'Right-Hand'),
        ('Left-Hand', 'Left-Hand'),
    )
    BOWLING_STYLE_CHOICES = (
        ('Right-Arm Fast', 'Right-Arm Fast'),
        ('Right-Arm Medium', 'Right-Arm Medium'),
        ('Right-Arm Spin', 'Right-Arm Spin'),
        ('Left-Arm Fast', 'Left-Arm Fast'),
        ('Left-Arm Medium', 'Left-Arm Medium'),
        ('Left-Arm Spin', 'Left-Arm Spin'),
        ('None', 'None'),
    )

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Batsman')
    batting_style = models.CharField(max_length=30, choices=BATTING_STYLE_CHOICES, default='Right-Hand')
    bowling_style = models.CharField(max_length=30, choices=BOWLING_STYLE_CHOICES, default='None')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Match(models.Model):
    MATCH_TYPE_CHOICES = (
        ('T20', 'Twenty20'),
        ('ODI', 'One Day International'),
        ('Test', 'Test Match'),
    )
    STATUS_CHOICES = (
        ('Scheduled', 'Scheduled'),
        ('Live', 'Live'),
        ('Completed', 'Completed'),
        ('Abandoned', 'Abandoned'),
    )
    TOSS_DECISION_CHOICES = (
        ('Bat', 'Bat'),
        ('Bowl', 'Bowl'),
    )

    title = models.CharField(max_length=150, help_text="e.g., India vs Australia - 1st T20I")
    team_a = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_a')
    team_b = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_b')
    match_type = models.CharField(max_length=10, choices=MATCH_TYPE_CHOICES, default='T20')
    overs_limit = models.IntegerField(default=20, help_text="Total overs per innings")
    venue = models.CharField(max_length=100)
    date = models.DateTimeField()
    toss_winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='toss_won_matches')
    toss_decision = models.CharField(max_length=10, choices=TOSS_DECISION_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_matches')
    result_margin = models.CharField(max_length=100, null=True, blank=True, help_text="e.g., IND won by 10 runs")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

class MatchInnings(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='innings')
    batting_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_innings')
    bowling_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='bowling_innings')
    innings_number = models.IntegerField(default=1, help_text="1 or 2")
    total_runs = models.IntegerField(default=0)
    total_wickets = models.IntegerField(default=0)
    total_balls = models.IntegerField(default=0, help_text="Number of legal balls bowled")
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('match', 'innings_number')

    def __str__(self):
        return f"{self.match.title} - Innings {self.innings_number} ({self.batting_team.short_name})"

    @property
    def overs(self):
        completed_overs = self.total_balls // 6
        remaining_balls = self.total_balls % 6
        return f"{completed_overs}.{remaining_balls}"

    @property
    def run_rate(self):
        if self.total_balls == 0:
            return 0.0
        overs_float = (self.total_balls / 6.0)
        return round(self.total_runs / overs_float, 2)

class BattingScorecard(models.Model):
    DISMISSAL_CHOICES = (
        ('DNB', 'Did Not Bat'),
        ('Not Out', 'Not Out'),
        ('Bowled', 'Bowled'),
        ('Caught', 'Caught'),
        ('LBW', 'LBW'),
        ('Run Out', 'Run Out'),
        ('Stumped', 'Stumped'),
        ('Retired Hurt', 'Retired Hurt'),
        ('Hit Wicket', 'Hit Wicket'),
    )

    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='batting_cards')
    innings = models.ForeignKey(MatchInnings, on_delete=models.CASCADE, related_name='batsmen_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batting_stats')
    runs = models.IntegerField(default=0)
    balls_faced = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    dismissal_status = models.CharField(max_length=30, choices=DISMISSAL_CHOICES, default='DNB')
    dismissed_by = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='batting_wickets_taken')
    fielder = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='batting_catches_taken')

    class Meta:
        unique_together = ('innings', 'player')

    def __str__(self):
        return f"{self.player.full_name} - {self.runs}({self.balls_faced}) - {self.dismissal_status}"

    @property
    def strike_rate(self):
        if self.balls_faced == 0:
            return 0.0
        return round((self.runs / self.balls_faced) * 100, 2)

class BowlingScorecard(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='bowling_cards')
    innings = models.ForeignKey(MatchInnings, on_delete=models.CASCADE, related_name='bowlers_stats')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowling_stats')
    balls_bowled = models.IntegerField(default=0, help_text="Number of legal balls bowled")
    runs_conceded = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    maidens = models.IntegerField(default=0)
    wides_bowled = models.IntegerField(default=0)
    noballs_bowled = models.IntegerField(default=0)

    class Meta:
        unique_together = ('innings', 'player')

    def __str__(self):
        return f"{self.player.full_name} - {self.wickets}/{self.runs_conceded} in {self.overs}"

    @property
    def overs(self):
        completed_overs = self.balls_bowled // 6
        remaining_balls = self.balls_bowled % 6
        return f"{completed_overs}.{remaining_balls}"

    @property
    def economy_rate(self):
        if self.balls_bowled == 0:
            return 0.0
        overs_float = (self.balls_bowled / 6.0)
        return round(self.runs_conceded / overs_float, 2)

class BallByBall(models.Model):
    EXTRA_CHOICES = (
        ('None', 'None'),
        ('Wide', 'Wide'),
        ('No Ball', 'No Ball'),
        ('Leg Bye', 'Leg Bye'),
        ('Bye', 'Bye'),
    )
    WICKET_TYPE_CHOICES = (
        ('None', 'None'),
        ('Bowled', 'Bowled'),
        ('Caught', 'Caught'),
        ('LBW', 'LBW'),
        ('Run Out', 'Run Out'),
        ('Stumped', 'Stumped'),
        ('Retired Hurt', 'Retired Hurt'),
        ('Hit Wicket', 'Hit Wicket'),
    )

    innings = models.ForeignKey(MatchInnings, on_delete=models.CASCADE, related_name='deliveries')
    over_number = models.IntegerField(help_text="0-indexed (e.g. 0 for first over, 19 for 20th over)")
    ball_number = models.IntegerField(help_text="1 to 6 (or higher for extra balls like wides/no balls)")
    batsman = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batting_deliveries')
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowling_deliveries')
    non_striker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='non_striker_deliveries')
    runs_batsman = models.IntegerField(default=0, help_text="Runs scored off the bat")
    runs_extras = models.IntegerField(default=0, help_text="Extra runs (from wides, no-balls, byes, etc.)")
    extra_type = models.CharField(max_length=20, choices=EXTRA_CHOICES, default='None')
    wicket = models.BooleanField(default=False)
    wicket_type = models.CharField(max_length=20, choices=WICKET_TYPE_CHOICES, default='None')
    dismissed_player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='dismissals')
    fielder = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='assisting_dismissals', help_text="Fielder who took the catch/stumped/runout")
    commentary = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['over_number', 'ball_number']
        unique_together = ('innings', 'over_number', 'ball_number')

    def __str__(self):
        extra_info = f" ({self.extra_type})" if self.extra_type != 'None' else ""
        wicket_info = f" - WICKET ({self.wicket_type})" if self.wicket else ""
        return f"Over {self.over_number}.{self.ball_number}: {self.bowler.last_name} to {self.batsman.last_name} - {self.runs_batsman + self.runs_extras} runs{extra_info}{wicket_info}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically trigger innings scorecard recalculation on every save!
        recalculate_innings_scorecard(self.innings)

    def delete(self, *args, **kwargs):
        innings = self.innings
        super().delete(*args, **kwargs)
        # Automatically trigger innings scorecard recalculation on deletion!
        recalculate_innings_scorecard(innings)


def recalculate_innings_scorecard(innings):
    """
    Recalculates the entire MatchInnings, BattingScorecard, and BowlingScorecard tables 
    from the current list of deliveries in the database.
    """
    deliveries = innings.deliveries.all().order_by('over_number', 'ball_number')

    # Reset Innings stats
    innings.total_runs = 0
    innings.total_wickets = 0
    innings.total_balls = 0

    batsmen_stats = {}
    bowlers_stats = {}
    overs_data = {}

    for delivery in deliveries:
        is_wide = (delivery.extra_type == 'Wide')
        is_noball = (delivery.extra_type == 'No Ball')
        is_legal = not (is_wide or is_noball)

        runs_batsman = delivery.runs_batsman
        runs_extras = delivery.runs_extras
        total_ball_runs = runs_batsman + runs_extras

        # Innings runs & wickets
        innings.total_runs += total_ball_runs
        if delivery.wicket:
            innings.total_wickets += 1

        if is_legal:
            innings.total_balls += 1

        # Batsman dynamic stats
        bat_id = delivery.batsman.id
        if bat_id not in batsmen_stats:
            batsmen_stats[bat_id] = {
                'runs': 0, 'balls_faced': 0, 'fours': 0, 'sixes': 0,
                'dismissal_status': 'Not Out', 'dismissed_by': None, 'fielder': None
            }

        # Batsman balls faced (faces everything except Wide balls)
        if not is_wide:
            batsmen_stats[bat_id]['balls_faced'] += 1

        batsmen_stats[bat_id]['runs'] += runs_batsman
        if runs_batsman == 4:
            batsmen_stats[bat_id]['fours'] += 1
        elif runs_batsman == 6:
            batsmen_stats[bat_id]['sixes'] += 1

        # Non striker list registration (in case they didn't bat but were on field)
        non_strike_id = delivery.non_striker.id
        if non_strike_id not in batsmen_stats:
            batsmen_stats[non_strike_id] = {
                'runs': 0, 'balls_faced': 0, 'fours': 0, 'sixes': 0,
                'dismissal_status': 'Not Out', 'dismissed_by': None, 'fielder': None
            }

        # Handle dismissal details
        if delivery.wicket and delivery.dismissed_player:
            d_id = delivery.dismissed_player.id
            if d_id not in batsmen_stats:
                batsmen_stats[d_id] = {
                    'runs': 0, 'balls_faced': 0, 'fours': 0, 'sixes': 0,
                    'dismissal_status': 'Not Out', 'dismissed_by': None, 'fielder': None
                }
            batsmen_stats[d_id]['dismissal_status'] = delivery.wicket_type
            
            # Bowler gets credit if it's not a runout or retired hurt
            if delivery.wicket_type not in ['Run Out', 'Retired Hurt']:
                batsmen_stats[d_id]['dismissed_by'] = delivery.bowler
            
            # Fielder gets credit for Caught, Stumped, Run Out
            if delivery.wicket_type in ['Caught', 'Stumped', 'Run Out'] and delivery.fielder:
                batsmen_stats[d_id]['fielder'] = delivery.fielder

        # Bowler dynamic stats
        bowl_id = delivery.bowler.id
        if bowl_id not in bowlers_stats:
            bowlers_stats[bowl_id] = {
                'balls_bowled': 0, 'runs_conceded': 0, 'wickets': 0,
                'wides_bowled': 0, 'noballs_bowled': 0, 'maidens': 0
            }

        if is_legal:
            bowlers_stats[bowl_id]['balls_bowled'] += 1

        # Bowler runs concession: Wides, No Balls, and Batsman runs count against the bowler.
        # Leg Byes and Byes do NOT count against the bowler.
        bowler_run_charge = runs_batsman
        if delivery.extra_type in ['Wide', 'No Ball']:
            bowler_run_charge += runs_extras

        bowlers_stats[bowl_id]['runs_conceded'] += bowler_run_charge

        if delivery.extra_type == 'Wide':
            bowlers_stats[bowl_id]['wides_bowled'] += 1
        elif delivery.extra_type == 'No Ball':
            bowlers_stats[bowl_id]['noballs_bowled'] += 1

        # Bowler wickets credit
        if delivery.wicket and delivery.wicket_type in ['Bowled', 'Caught', 'LBW', 'Stumped', 'Hit Wicket']:
            bowlers_stats[bowl_id]['wickets'] += 1

        # Track overs for maidens calculation
        ov = delivery.over_number
        if ov not in overs_data:
            overs_data[ov] = {'legal_balls': 0, 'bowler_runs': 0, 'bowler_id': bowl_id}
        
        if is_legal:
            overs_data[ov]['legal_balls'] += 1
        overs_data[ov]['bowler_runs'] += bowler_run_charge

    # Calculate maidens: completed over (6 legal balls) with 0 bowler runs conceded
    for ov, data in overs_data.items():
        if data['legal_balls'] == 6 and data['bowler_runs'] == 0:
            b_id = data['bowler_id']
            if b_id in bowlers_stats:
                bowlers_stats[b_id]['maidens'] += 1

    # Save Innings
    innings.save()

    # Re-sync scorecard database
    # Deleting old scorecards first guarantees zero duplicate/stale records!
    BattingScorecard.objects.filter(innings=innings).delete()
    BowlingScorecard.objects.filter(innings=innings).delete()

    for p_id, stats in batsmen_stats.items():
        # Only save batting card if they actually faced a ball or got dismissed (or were striker/nonstriker)
        # (This is standard cricket, players who DNB are generally omitted or shown separately)
        BattingScorecard.objects.create(
            match=innings.match,
            innings=innings,
            player_id=p_id,
            runs=stats['runs'],
            balls_faced=stats['balls_faced'],
            fours=stats['fours'],
            sixes=stats['sixes'],
            dismissal_status=stats['dismissal_status'],
            dismissed_by=stats['dismissed_by'],
            fielder=stats['fielder']
        )

    for p_id, stats in bowlers_stats.items():
        BowlingScorecard.objects.create(
            match=innings.match,
            innings=innings,
            player_id=p_id,
            balls_bowled=stats['balls_bowled'],
            runs_conceded=stats['runs_conceded'],
            wickets=stats['wickets'],
            maidens=stats['maidens'],
            wides_bowled=stats['wides_bowled'],
            noballs_bowled=stats['noballs_bowled']
        )
