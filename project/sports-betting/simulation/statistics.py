"""
This module is for calculating the statistics for strategies
including but not limited too

- the risk reward spread
- plotting performance over time
- other things I guess?
"""
from typing import List

from simulation.types import Bet, BetOffer


def risk_reward_spread():
    pass


def calculate_vig(bets: List[Bet]) -> float:
    pass


def calculate_fractional_odds(bet: Bet) -> float:
    value: float
    odds = bet.bet_offer.odds
    if odds > 0:
        value = odds / 100
    else:
        value = -100 / odds
    return value


def calculate_demical_odds(bet: BetOffer) -> float:
    value: float
    odds = bet.odds
    if odds > 0:
        value = odds / 100
    else:
        value = -100 / odds
    return value + 1


def calculate_implied_probability(bet: Bet) -> float:
    value: float
    odds = bet.bet_offer.odds
    if odds > 0:
        value = 100 / (odds + 100)
    else:
        odds *= -1
        value = odds / (odds + 100)
    return value


def calculate_payout(bet: Bet) -> float:
    return bet.wager + round(bet.wager * calculate_fractional_odds(bet), 2)
