import os
import sys
import json
import django

# 1. Setup Django Environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scorecard_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from scorecard.models import Team, Player, Match, MatchInnings, BattingScorecard, BowlingScorecard, BallByBall

def run_verification():
    print("======================================================================")
    print("               CRICKET SCORECARD API VERIFICATION SCRIPT             ")
    print("======================================================================")

    # 1. Verify Seed Data
    print("\n--- [1] Checking Seed Data ---")
    teams = Team.objects.all()
    print(f"Total Teams: {teams.count()}")
    for t in teams:
        print(f" - {t.name} ({t.short_name}) with {t.players.count()} players")

    matches = Match.objects.all()
    print(f"Total Matches: {matches.count()}")
    match = matches.first()
    print(f"Seeded Match: '{match.title}' at {match.venue}")

    scorer = User.objects.get(username='scorer')
    token = Token.objects.get(user=scorer)
    print(f"Scorer username: {scorer.username}")
    print(f"Scorer Token: {token.key}")

    # 2. Setup DRF API Client
    print("\n--- [2] Testing DRF API Client Authenticated Actions ---")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # Resolve players for live gameplay
    india = Team.objects.get(short_name="IND")
    australia = Team.objects.get(short_name="AUS")
    
    batsman1 = Player.objects.get(first_name="Rohit", last_name="Sharma")
    batsman2 = Player.objects.get(first_name="Virat", last_name="Kohli")
    bowler1 = Player.objects.get(first_name="Mitchell", last_name="Starc")
    fielder1 = Player.objects.get(first_name="Pat", last_name="Cummins")

    print(f"Striker Batsman: {batsman1.full_name}")
    print(f"Non-Striker Batsman: {batsman2.full_name}")
    print(f"Bowler: {bowler1.full_name}")

    # Start Innings 1 via API
    print(f"\n--- [3] POST: /api/matches/{match.id}/start_innings/ ---")
    start_payload = {
        "innings_number": 1,
        "batting_team": india.id
    }
    response = client.post(f"/api/matches/{match.id}/start_innings/", start_payload, format='json')
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))

    # 3. Simulate recording balls (Over 0)
    print(f"\n--- [4] Simulating live ball-by-ball recording ---")
    
    # Ball 0.1: 1 run off the bat
    ball_1 = {
        "innings_number": 1,
        "over_number": 0,
        "ball_number": 1,
        "batsman": batsman1.id,
        "non_striker": batsman2.id,
        "bowler": bowler1.id,
        "runs_batsman": 1,
        "runs_extras": 0,
        "extra_type": "None",
        "commentary": "Starc starts with a full length delivery, Rohit guides it to third man for a single."
    }
    
    # Ball 0.2: Wide ball (extra 1 run)
    ball_2_wide = {
        "innings_number": 1,
        "over_number": 0,
        "ball_number": 2,
        "batsman": batsman2.id, # Virat Kohli on strike now
        "non_striker": batsman1.id,
        "bowler": bowler1.id,
        "runs_batsman": 0,
        "runs_extras": 1,
        "extra_type": "Wide",
        "commentary": "Starc sprays this down the leg side, wide called by the umpire."
    }

    # Ball 0.3 (rebowled): 4 runs (four!)
    ball_2_legal = {
        "innings_number": 1,
        "over_number": 0,
        "ball_number": 3,
        "batsman": batsman2.id,
        "non_striker": batsman1.id,
        "bowler": bowler1.id,
        "runs_batsman": 4,
        "runs_extras": 0,
        "extra_type": "None",
        "commentary": "CRACK! Virat Kohli takes toll of a half volley, driven beautifully through extra cover for a boundary!"
    }

    # Ball 0.4: Wicket (Caught by Cummins)
    ball_3_wicket = {
        "innings_number": 1,
        "over_number": 0,
        "ball_number": 4,
        "batsman": batsman2.id,
        "non_striker": batsman1.id,
        "bowler": bowler1.id,
        "runs_batsman": 0,
        "runs_extras": 0,
        "extra_type": "None",
        "wicket": True,
        "wicket_type": "Caught",
        "dismissed_player": batsman2.id,
        "fielder": fielder1.id,
        "commentary": "OUT! Starc strikes! Kohli attempts another drive but gets a thick edge. Pat Cummins takes a sharp catch at second slip!"
    }

    deliveries_to_record = [ball_1, ball_2_wide, ball_2_legal, ball_3_wicket]
    
    for idx, ball_data in enumerate(deliveries_to_record, 1):
        print(f"\nRecording Ball {idx}...")
        resp = client.post(f"/api/matches/{match.id}/record_ball/", ball_data, format='json')
        print(f"Status Code: {resp.status_code}")
        summary = resp.json().get("innings_summary", {})
        print(f"Innings Status after ball: Runs: {summary.get('total_runs')}, Wickets: {summary.get('total_wickets')}, Overs: {summary.get('overs')}, Run Rate: {summary.get('run_rate')}")

    # 4. Read full scorecard
    print(f"\n--- [5] GET: /api/matches/{match.id}/scorecard/ ---")
    # Public endpoint (test anonymous client)
    anon_client = APIClient()
    score_resp = anon_client.get(f"/api/matches/{match.id}/scorecard/")
    print(f"Status Code: {score_resp.status_code}")
    score_data = score_resp.json()
    
    # Print a beautiful visual scorecard representation
    print("\n=======================================================")
    print(f" MATCH SCORECARD: {score_data['title'].upper()}")
    print(f" Venue: {score_data['venue']} | Status: {score_data['status']}")
    print("=======================================================")
    
    for inn in score_data['innings']:
        print(f"\nINNINGS {inn['innings_number']}: {inn['batting_team_name']} vs {inn['bowling_team_name']}")
        print(f"Score: {inn['total_runs']}/{inn['total_wickets']} in {inn['overs']} overs (RR: {inn['run_rate']})")
        print("\nBATTING CARD:")
        print(f"{'Batsman':<25} {'Status':<15} {'Runs':<5} {'Balls':<5} {'4s':<3} {'6s':<3} {'SR':<6}")
        print("-" * 70)
        for bat in inn['batsmen_stats']:
            status_str = bat['dismissal_status']
            if status_str != 'Not Out' and status_str != 'DNB':
                status_str = f"c {bat['fielder_name']} b {bat['dismissed_by_name']}" if bat['fielder_name'] else f"b {bat['dismissed_by_name']}"
            print(f"{bat['player_name']:<25} {status_str:<15} {bat['runs']:<5} {bat['balls_faced']:<5} {bat['fours']:<3} {bat['sixes']:<3} {bat['strike_rate']:<6}")
            
        print("\nBOWLING CARD:")
        print(f"{'Bowler':<25} {'Overs':<6} {'Maidens':<8} {'Runs':<5} {'Wickets':<8} {'Econ':<5}")
        print("-" * 70)
        for bowl in inn['bowlers_stats']:
            print(f"{bowl['player_name']:<25} {bowl['overs']:<6} {bowl['maidens']:<8} {bowl['runs_conceded']:<5} {bowl['wickets']:<8} {bowl['economy_rate']:<5}")
            
        print("\nBALL BY BALL COMMENTARY:")
        for ball in inn['deliveries']:
            wicket_text = " [WICKET]" if ball['wicket'] else ""
            print(f" {ball['over_number']}.{ball['ball_number']}: {ball['commentary']}{wicket_text}")
    print("\n=======================================================")
    print("                  VERIFICATION COMPLETED               ")
    print("=======================================================")

if __name__ == "__main__":
    run_verification()
