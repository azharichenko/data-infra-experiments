from typing import List, Optional

from simulation.statistics import calculate_demical_odds, calculate_payout
from simulation.strategy import BaseStrategy
from simulation.types import Bet, Game


class HomeTeamWinsMoneyLine(BaseStrategy):
    def make_bet_offer(self, game: Game) -> List[Bet]:
        bet_offer = game.game_odds.moneyline[0]
        return [
            Bet(bet_offer=bet_offer, wager=self.betting_unit_size),
        ]


class AwayTeamWinsMoneyLine(BaseStrategy):
    def make_bet_offer(self, game: Game) -> List[Bet]:
        bet_offer = game.game_odds.moneyline[1]
        return [
            Bet(bet_offer=bet_offer, wager=self.betting_unit_size),
        ]


class HomeTeamWinsRegularTime(BaseStrategy):
    def make_bet_offer(self, game: Game) -> List[Bet]:
        bet_offer = game.game_odds.regular_time[0]
        return [
            Bet(bet_offer=bet_offer, wager=self.betting_unit_size),
        ]


class AwayTeamWinsRegularTime(BaseStrategy):
    def make_bet_offer(self, game: Game) -> List[Bet]:
        bet_offer = game.game_odds.regular_time[1]
        return [
            Bet(bet_offer=bet_offer, wager=self.betting_unit_size),
        ]


class NoTiesRegularTime(BaseStrategy):
    def make_bet_offer(self, game: Game) -> List[Bet]:
        return [
            Bet(bet_offer=bet_offer, wager=self.betting_unit_size)
            for bet_offer in game.game_odds.regular_time
        ]


class HomeWinWithOpposingHedgeRegularTime(BaseStrategy):
    def make_bet_offer(self, game: Game) -> List[Bet]:
        home_odds = [
            bet_offer
            for bet_offer in game.game_odds.regular_time
            if bet_offer.team == game.home_team
        ]
        home_decimal_odds = calculate_demical_odds(home_odds[0])
        return [
            Bet(
                bet_offer=bet_offer,
                wager=self.betting_unit_size
                if bet_offer.team == game.home_team
                else round(home_decimal_odds / calculate_demical_odds(bet_offer), 2)
                + 0.01,
            )
            for bet_offer in game.game_odds.regular_time
        ]


# class HomeWinWithOpposingHedgeMoneyLine(BaseStrategy):
#     def make_bet_offer(self, game: Game) -> List[Bet]:
#         home_bet_offer, away_bet_offer = game.game_odds.moneyline
#         home_bet = Bet(bet_offer=home_bet_offer, wager=self.betting_unit_size)
#         away_bet = Bet(
#             bet_offer=away_bet_offer,
#             wager=round(
#                 100 * (calculate_payout(home_bet) / (away_bet_offer.odds + 100)), 2
#             ),
#         )
#         return [home_bet, away_bet]
