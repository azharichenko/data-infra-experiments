from datetime import date
from enum import Enum, IntEnum
from typing import List, NamedTuple


class Team(str, Enum):
    PHI = "PHI Flyers"
    TB = "TB Lightning"
    BOS = "BOS Bruins"
    BUF = "BUF Sabres"
    EDM = "EDM Oilers"
    DAL = "DAL Stars"
    CGY = "CGY Flames"
    CHI = "CHI Blackhawks"
    NY = "NY Rangers"
    MIN = "MIN Wild"
    WPG = "WPG Jets"
    STL = "STL Blues"
    CAR = "CAR Hurricanes"
    ANA = "ANA Ducks"
    OTT = "OTT Senators"
    WSH = "WSH Capitals"
    FLA = "FLA Panthers"
    NSH = "NSH Predators"
    NJ = "NJ Devils"
    CBJ = "CBJ Blue Jackets"
    VAN = "VAN Canucks"
    MTL = "MTL Canadiens"
    SEA = "SEA Kraken"
    COL = "COL Avalanche"
    TOR = "TOR Maple Leafs"

    def __repr__(self):
        return self.name


class NHLGameOutcome(Enum):
    HOME_TEAM_WIN_REGULAR_TIME = 1
    AWAY_TEAM_WIN_REGULAR_TIME = 2
    HOME_TEAM_WIN_OT = 3
    AWAY_TEAM_WIN_OT = 4


class Outcome(IntEnum):
    FULL_GAME_GOALS = 1
    REGULAR_TIME_GOALS = 2


class BetType(IntEnum):
    MONEYLINE = Outcome.FULL_GAME_GOALS
    REGULAR_TIME = Outcome.REGULAR_TIME_GOALS
    NO_TIE_BET = Outcome.REGULAR_TIME_GOALS

    def __repr__(self):
        return self.name


class BetOffer(NamedTuple):
    rivers_id: int
    team: Team
    bet_type: BetType
    odds: int


class Bet(NamedTuple):
    bet_offer: BetOffer
    wager: float


class GameOdds(NamedTuple):
    tie_no_bet: List[BetOffer]
    regular_time: List[BetOffer]
    moneyline: List[BetOffer]


class GameOutcome(NamedTuple):
    winning_team: Team
    regular_game_tie: bool


class Game(NamedTuple):
    rivers_id: int
    start_datetime: date
    home_team: Team
    away_team: Team
    game_odds: GameOdds
