from abc import ABC, abstractclassmethod, abstractmethod
from typing import List

from simulation.models import Strategy
from simulation.types import Game, Bet


class BaseStrategy(ABC):
    MINIMUM_BET = 0.10

    def __init__(self, database_id, starting_bankroll, betting_unit_size) -> None:
        self.id = database_id
        self.starting_bankroll = starting_bankroll
        self.betting_unit_size = betting_unit_size

        self.open_bets_made: List[Bet] = []
        self.bankroll = 100

    # TODO: Create class method that fetches and constrcuts a strategy that morphs
    # with an idea that is present in the database

    @classmethod
    def get_instance(cls) -> "BaseStrategy":
        strategy_class_name = cls.__name__
        data_model: Strategy
        try:
            data_model = Strategy.get(name=strategy_class_name)

        except Exception:
            data_model = Strategy.create(
                name=strategy_class_name, starting_bankroll=100, betting_unit_size=1
            )
            data_model.save()

        return cls(
            database_id=data_model.id,
            starting_bankroll=data_model.starting_bankroll,
            betting_unit_size=data_model.betting_unit_size,
        )

    @abstractmethod
    def make_bet_offer(self, game: Game) -> List[Bet]:
        pass

    def betting_units_available(self) -> float:
        return self.bankroll / self.betting_unit_size

    def is_alive(self) -> bool:
        return (
            self.betting_units_available() > 1
            and self.bankroll > BaseStrategy.MINIMUM_BET
        )
