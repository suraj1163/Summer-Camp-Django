from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token
from scorecard.models import Team, Player, Match

User = get_user_model()

class Command(BaseCommand):
    help = "Seeds the database with a default scorer, cricket teams, players, and a match."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("--- SEEDING CRICKET SCORECARD DATABASE ---"))

        # 1. Create Scorer User
        scorer_username = 'scorer'
        scorer_email = 'scorer@cricketscorecard.com'
        scorer_pass = 'scorer123'
        
        scorer, created = User.objects.get_or_create(
            username=scorer_username,
            defaults={'email': scorer_email, 'first_name': 'Official', 'last_name': 'Scorer'}
        )
        if created:
            scorer.set_password(scorer_pass)
            scorer.save()
            self.stdout.write(self.style.SUCCESS(f"Created Scorer user: '{scorer_username}' with password: '{scorer_pass}'"))
        else:
            self.stdout.write(f"Scorer user '{scorer_username}' already exists.")

        # Create/Get token
        token, _ = Token.objects.get_or_create(user=scorer)
        self.stdout.write(self.style.SUCCESS(f"Authentication Token for scorer: {token.key}"))

        # 2. Create Teams
        ind_team, ind_created = Team.objects.get_or_create(name="India", short_name="IND")
        aus_team, aus_created = Team.objects.get_or_create(name="Australia", short_name="AUS")
        
        self.stdout.write(f"Team: {ind_team}")
        self.stdout.write(f"Team: {aus_team}")

        # 3. Create Players
        ind_players = [
            ("Rohit", "Sharma", "Batsman", "Right-Hand", "None"),
            ("Yashasvi", "Jaiswal", "Batsman", "Left-Hand", "None"),
            ("Virat", "Kohli", "Batsman", "Right-Hand", "None"),
            ("Suryakumar", "Yadav", "Batsman", "Right-Hand", "None"),
            ("Rishabh", "Pant", "Wicket-Keeper", "Left-Hand", "None"),
            ("Hardik", "Pandya", "All-Rounder", "Right-Hand", "Right-Arm Fast"),
            ("Ravindra", "Jadeja", "All-Rounder", "Left-Hand", "Left-Arm Spin"),
            ("Axar", "Patel", "All-Rounder", "Left-Hand", "Left-Arm Spin"),
            ("Kuldeep", "Yadav", "Bowler", "Left-Hand", "Left-Arm Spin"),
            ("Jasprit", "Bumrah", "Bowler", "Right-Hand", "Right-Arm Fast"),
            ("Arshdeep", "Singh", "Bowler", "Left-Hand", "Left-Arm Fast"),
        ]

        aus_players = [
            ("Travis", "Head", "Batsman", "Left-Hand", "Right-Arm Spin"),
            ("David", "Warner", "Batsman", "Left-Hand", "None"),
            ("Mitchell", "Marsh", "All-Rounder", "Right-Hand", "Right-Arm Medium"),
            ("Glenn", "Maxwell", "All-Rounder", "Right-Hand", "Right-Arm Spin"),
            ("Marcus", "Stoinis", "All-Rounder", "Right-Hand", "Right-Arm Medium"),
            ("Tim", "David", "Batsman", "Right-Hand", "None"),
            ("Matthew", "Wade", "Wicket-Keeper", "Left-Hand", "None"),
            ("Pat", "Cummins", "Bowler", "Right-Hand", "Right-Arm Fast"),
            ("Mitchell", "Starc", "Bowler", "Left-Hand", "Left-Arm Fast"),
            ("Adam", "Zampa", "Bowler", "Right-Hand", "Right-Arm Spin"),
            ("Josh", "Hazlewood", "Bowler", "Right-Hand", "Right-Arm Fast"),
        ]

        # Populate India Players
        for fn, ln, role, bat, bowl in ind_players:
            player, p_created = Player.objects.get_or_create(
                first_name=fn, last_name=ln,
                defaults={'team': ind_team, 'role': role, 'batting_style': bat, 'bowling_style': bowl}
            )
            if p_created:
                self.stdout.write(f"Added India player: {player}")

        # Populate Australia Players
        for fn, ln, role, bat, bowl in aus_players:
            player, p_created = Player.objects.get_or_create(
                first_name=fn, last_name=ln,
                defaults={'team': aus_team, 'role': role, 'batting_style': bat, 'bowling_style': bowl}
            )
            if p_created:
                self.stdout.write(f"Added Australia player: {player}")

        # 4. Create Match
        match, m_created = Match.objects.get_or_create(
            title="India vs Australia - ICC T20 World Cup Final",
            defaults={
                'team_a': ind_team,
                'team_b': aus_team,
                'match_type': 'T20',
                'overs_limit': 20,
                'venue': 'Kensington Oval, Bridgetown, Barbados',
                'date': timezone.now() + timezone.timedelta(days=1),
                'toss_winner': ind_team,
                'toss_decision': 'Bat',
                'status': 'Scheduled'
            }
        )

        if m_created:
            self.stdout.write(self.style.SUCCESS(f"Created scheduled match: '{match.title}' at {match.venue}"))
        else:
            self.stdout.write(f"Match '{match.title}' already exists.")

        self.stdout.write(self.style.SUCCESS("--- DATABASE SEEDING COMPLETED ---"))
