"""
Race for the Galaxy - Core module

This module provides the core game engine and data structures for
the Python implementation of Race for the Galaxy.
"""

from .constants import *
from .game_state import (
    GameState, Player, Card, Design, Power, VPBonus,
    CardType, GoodType, CardLocation, GamePhase, ActionChoice, PowerType
)
from .engine import GameEngine

__version__ = VERSION
__all__ = [
    # Constants
    'VERSION', 'MAX_PLAYER', 'MAX_DECK', 'MAX_POWER', 'MAX_VP_BONUS',
    'MAX_TAKEOVER', 'MAX_EXPANSION', 'MAX_PHASE', 'MAX_ACTION', 'MAX_GOOD',
    'MAX_WHERE', 'MAX_SEARCH', 'MAX_GOAL',
    
    # Card flags
    'FLAG_MILITARY', 'FLAG_WINDFALL', 'FLAG_START', 'FLAG_START_RED',
    'FLAG_START_BLUE', 'FLAG_PROMO', 'FLAG_REBEL', 'FLAG_UPLIFT',
    'FLAG_ALIEN', 'FLAG_TERRAFORMING', 'FLAG_IMPERIUM', 'FLAG_CHROMO',
    'FLAG_PRESTIGE', 'FLAG_STARTHAND_3', 'FLAG_START_SAVE',
    'FLAG_DISCARD_TO_12', 'FLAG_GAME_END_14', 'FLAG_TAKE_DISCARDS',
    'FLAG_SELECT_LAST', 'FLAG_EXTRA_SURVEY', 'FLAG_NO_PRODUCE',
    'FLAG_DISCARD_PRODUCE', 'FLAG_XENO', 'FLAG_ANTI_XENO', 'FLAG_PEACEFUL',
    
    # Good types
    'GOOD_ANY', 'GOOD_NOVELTY', 'GOOD_RARE', 'GOOD_GENE', 'GOOD_ALIEN',
    
    # Locations
    'WHERE_DECK', 'WHERE_DISCARD', 'WHERE_HAND', 'WHERE_ACTIVE',
    'WHERE_GOOD', 'WHERE_VP', 'WHERE_SAVED', 'WHERE_PRESTIGE',
    
    # Phases
    'PHASE_ACTION', 'PHASE_EXPLORE', 'PHASE_DEVELOP', 'PHASE_SETTLE',
    'PHASE_CONSUME', 'PHASE_PRODUCE', 'PHASE_DISCARD',
    
    # Actions
    'ACT_GAME_START', 'ACT_ROUND_START', 'ACT_SEARCH', 'ACT_EXPLORE_5_0',
    'ACT_EXPLORE_1_1', 'ACT_DEVELOP', 'ACT_DEVELOP2', 'ACT_SETTLE',
    'ACT_SETTLE2', 'ACT_CONSUME_TRADE', 'ACT_CONSUME_X2', 'ACT_PRODUCE',
    'ACT_ROUND_END', 'ACT_MASK', 'ACT_PRESTIGE',
    
    # Power types
    'P_DISCARD', 'P_CONSUME_HAND', 'P_CONSUME_GOOD', 'P_CONSUME_PRESTIGE',
    'P_TEMPORARY', 'P_GAME_START', 'P_PREPARE', 'P_START', 'P_PLACE',
    'P_CONSUME_3_DIFF', 'P_CONSUME_N_DIFF', 'P_CONSUME_ALL', 'P_PRODUCE',
    'P_PRODUCE_PRESTIGE', 'P_VP', 'P_TAKEOVER', 'P_END',
    
    # Enums
    'CardType', 'GoodType', 'CardLocation', 'GamePhase', 'ActionChoice',
    'PowerType',
    
    # Data structures
    'Power', 'VPBonus', 'Design', 'Card', 'Player', 'GameState',
    
    # Engine
    'GameEngine',
]
