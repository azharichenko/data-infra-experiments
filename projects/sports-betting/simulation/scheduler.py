import sched
import time
from typing import Type

from simulation.statistics import calculate_payout
from simulation.strategies import discover_strategies
from simulation.sportsbook import fetch_todays_games_odds
from simulation.strategy import BaseStrategy

s = sched.scheduler(time.time, time.sleep)


def compile_game_day_odds() -> None:
    """Fetch daily game odds and insert into database"""
    games = fetch_todays_games_odds()
    s.enter(delay=0, priority=0, action=execute_strategies)


def payout_outcome(is_home_team: bool, bet) -> float:
    if is_home_team:
        return calculate_payout(bet)
    return 0


def execute_strategies() -> None:
    games = fetch_todays_games_odds()
    for strategy in discover_strategies():
        s: BaseStrategy = strategy.get_instance()
        # s = strategy(100, 5)
        print(strategy.__name__)
        wager = 0
        for game in games:
            bets = s.make_bet_offer(game)

            for bet in bets:
                s.bankroll -= bet.wager
                s.bankroll += payout_outcome(game.home_team == bet.bet_offer.team, bet)
                wager += bet.wager
        print(
            "Ending Bankroll",
            s.bankroll,
            " | wager: ",
            wager,
            " profit/loss: ",
            round(s.bankroll - s.starting_bankroll, 2),
            round(s.bankroll - s.starting_bankroll, 2) / wager,
        )
        print()


def run_event_loop() -> None:
    s.enter(delay=0, priority=0, action=compile_game_day_odds)
