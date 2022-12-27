from enum import unique
from pathlib import Path

from peewee import (AutoField, CharField, DateTimeField, FloatField,
                    ForeignKeyField, IntegerField, IntegrityError, Model,
                    PrimaryKeyField, SqliteDatabase)
from simulation.types import Game as GameTuple
from simulation.types import GameOdds as GameOddsTuple
from simulation.types import Team

database_file = Path.cwd() / "data.sqlite"
database = SqliteDatabase(database_file)


class BaseModel(Model):
    class Meta:
        database = database


class Strategy(BaseModel):
    id = AutoField()
    name = CharField()
    starting_bankroll = FloatField()
    betting_unit_size = FloatField()


class Game(BaseModel):
    rivers_id = IntegerField(primary_key=True)
    start_datetime = DateTimeField()
    home_team = CharField()
    away_team = CharField()


class GameOdds(BaseModel):
    rivers_id = IntegerField(primary_key=True)
    game_id = ForeignKeyField(Game, backref="game")
    team = CharField()
    odds = IntegerField()


class Bets(BaseModel):
    executor = ForeignKeyField(Strategy, backref="strategy")
    game_odds_id = ForeignKeyField(GameOdds, backref="bet_odd")


def create_tables() -> None:
    with database:
        database.create_tables([Strategy, Game, GameOdds, Bets])


def insert_game_odds(game_id: int, odds: GameOddsTuple) -> None:
    with database:
        for set_of_odds in odds:
            for odd in set_of_odds:
                try:  # TODO: Catch that unqiue constraints
                    x = GameOdds.create(
                        game_id=game_id,
                        rivers_id=odd.rivers_id,
                        team=odd.team,
                        odds=odd.odds,
                    )
                    x.save()
                except:
                    pass


def insert_nhl_game(game: GameTuple):
    with database:
        try:
            Game.create(
                rivers_id=game.rivers_id,
                start_datetime=game.start_datetime,
                home_team=game.home_team,
                away_team=game.away_team,
            )
        except IntegrityError as e:
            if str(e) == "UNIQUE constraint failed: game.rivers_id":
                pass
            else:
                raise e

    insert_game_odds(game.rivers_id, game.game_odds)
