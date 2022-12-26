from datetime import timedelta, datetime
from typing import Dict, Iterable, List, Tuple

import requests
from simulation.models import insert_nhl_game

from simulation.types import Bet, GameOutcome, BetType, Team, BetOffer, Game, GameOdds

# TODO: Renames these for the love of god
URL = "https://pa.betrivers.com/api/service/sportsbook/offering/listview/events?pageNr=1&cageCode=268&groupId=1000093657&type=prematch"
OTHER_URL = "https://eu-offering.kambicdn.org/offering/v2018/rsi2uspa/betoffer/event/{game_id}.json?lang=en_US&market=US-PA&client_id=2&channel_id=1&ncid=1637530764386&includeParticipants=true"

EASTERN_TIMEDELTA = timedelta(hours=5)

bets = {
    # "Tie No Bet - Regular Time": BetType.NO_TIE_BET,  # TODO: What is happeing with this one
    "Regular Time Line (3-way)": BetType.REGULAR_TIME,
    "Moneyline - Inc. OT and Shootout": BetType.MONEYLINE,
}


def is_game_today(game_start_dt: datetime) -> bool:
    """Given game start time calculate whether the game is today"""
    game_date = game_start_dt.date()
    current_date = datetime.now().date()
    return game_date == current_date


def fetch_rivers_game_id() -> Iterable[Tuple[int, List[Dict], datetime]]:
    # TODO: Rename function to better name
    # TODO: Handle API Pagentation
    resp = requests.get(URL)
    data = resp.json()
    for item in data["items"]:
        game_dt = datetime.strptime(item["start"], "%Y-%m-%dT%H:%M:00.000Z")
        game_dt -= EASTERN_TIMEDELTA
        if item["state"] == "NOT_STARTED" and is_game_today(game_dt):
            yield int(item["id"]), item["participants"], game_dt


def parse_game_odds(game_odds: Dict) -> GameOdds:
    game_odds_data: Dict[str, List[BetOffer]] = {
        field: list() for field in GameOdds._fields
    }

    for bet_offer in game_odds["betOffers"]:
        bet_type = bet_offer["criterion"]["label"]
        if bet_type in bets:
            for outcome in bet_offer["outcomes"]:
                if "participant" in outcome:
                    x = bets[bet_type].name.lower()
                    game_odds_data[x].append(
                        BetOffer(
                            rivers_id=int(outcome["id"]),
                            team=Team(outcome["participant"]),
                            odds=int(outcome["oddsAmerican"]),
                            bet_type=bets[bet_type],
                        )
                    )
    return GameOdds(**game_odds_data)


def fetch_todays_games_odds() -> List[Game]:
    """Fetch games and the bet offers available today
    Only applies to games that have not started yet"""
    games: List[Game] = []

    for game_id, participants, game_dt in fetch_rivers_game_id():
        resp = requests.get(OTHER_URL.format(game_id=game_id))
        data = resp.json()
        away, home = participants
        odds = parse_game_odds(data)
        game = Game(
            rivers_id=game_id,
            start_datetime=game_dt,
            home_team=Team(home["name"]),
            away_team=Team(away["name"]),
            game_odds=odds,
        )
        insert_nhl_game(game)
        games.append(game)

    return games
