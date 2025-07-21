"""
Constants module for Race for the Galaxy

This module defines all the core constants exactly as specified in the
original C implementation to ensure perfect compatibility.
"""

from typing import Final

# System Constants - Must be preserved exactly
MAX_PLAYER: Final[int] = 6        # Maximum number of players
AVAILABLE_DESIGN: Final[int] = 300  # Available card design slots
MAX_DESIGN: Final[int] = 280      # Original card designs
MAX_DECK: Final[int] = 328        # Cards in deck
MAX_POWER: Final[int] = 5         # Powers per card
MAX_VP_BONUS: Final[int] = 6      # Special VP bonuses per card
MAX_TAKEOVER: Final[int] = 12     # Maximum pending takeovers
MAX_EXPANSION: Final[int] = 7     # Maximum expansions
MAX_PHASE: Final[int] = 7         # Number of phases
MAX_ACTION: Final[int] = 10       # Number of actions
MAX_GOOD: Final[int] = 6          # Number of good types
MAX_WHERE: Final[int] = 8         # Number of card locations
MAX_SEARCH: Final[int] = 9        # Maximum search results
MAX_GOAL: Final[int] = 20         # Maximum goals

# Version Information
VERSION: Final[str] = "0.9.5"     # Current version
COMM_VERSION: Final[str] = "0.9.4"  # Minimum compatible server version

# Card Flags - Must use exact 64-bit values
FLAG_MILITARY: Final[int] = 1 << 0          # Military world
FLAG_WINDFALL: Final[int] = 1 << 1          # Windfall world
FLAG_START: Final[int] = 1 << 2             # Starting world
FLAG_START_RED: Final[int] = 1 << 3         # Red starting world
FLAG_START_BLUE: Final[int] = 1 << 4        # Blue starting world
FLAG_PROMO: Final[int] = 1 << 5             # Promotional card
FLAG_REBEL: Final[int] = 1 << 6             # Rebel card
FLAG_UPLIFT: Final[int] = 1 << 7            # Uplift power
FLAG_ALIEN: Final[int] = 1 << 8             # Alien card
FLAG_TERRAFORMING: Final[int] = 1 << 9      # Terraforming power
FLAG_IMPERIUM: Final[int] = 1 << 10         # Imperium card
FLAG_CHROMO: Final[int] = 1 << 11           # Chromosome world
FLAG_PRESTIGE: Final[int] = 1 << 12         # Prestige card
FLAG_STARTHAND_3: Final[int] = 1 << 13      # Start with 3 in hand
FLAG_START_SAVE: Final[int] = 1 << 14       # Save at start
FLAG_DISCARD_TO_12: Final[int] = 1 << 15    # Discard to 12
FLAG_GAME_END_14: Final[int] = 1 << 16      # Game end at 14
FLAG_TAKE_DISCARDS: Final[int] = 1 << 17    # Take discards
FLAG_SELECT_LAST: Final[int] = 1 << 18      # Select last
FLAG_EXTRA_SURVEY: Final[int] = 1 << 19     # Extra survey
FLAG_NO_PRODUCE: Final[int] = 1 << 20       # Cannot produce
FLAG_DISCARD_PRODUCE: Final[int] = 1 << 21  # Discard to produce
FLAG_XENO: Final[int] = 1 << 22             # Xeno card
FLAG_ANTI_XENO: Final[int] = 1 << 23        # Anti-xeno card
FLAG_PEACEFUL: Final[int] = 1 << 24         # Peaceful card

# Good Types - Must use exact values
GOOD_ANY: Final[int] = 1          # Any good
GOOD_NOVELTY: Final[int] = 2      # Novelty good
GOOD_RARE: Final[int] = 3         # Rare good
GOOD_GENE: Final[int] = 4         # Gene good
GOOD_ALIEN: Final[int] = 5        # Alien good

# Card Locations - Must preserve exact values
WHERE_DECK: Final[int] = 0        # In draw deck
WHERE_DISCARD: Final[int] = 1     # In discard pile
WHERE_HAND: Final[int] = 2        # In player's hand
WHERE_ACTIVE: Final[int] = 3      # In player's tableau
WHERE_GOOD: Final[int] = 4        # Used as a good
WHERE_VP: Final[int] = 5          # Used to pay VP
WHERE_SAVED: Final[int] = 6       # Saved for later (special powers)
WHERE_PRESTIGE: Final[int] = 7    # Used to pay prestige

# Game Phases - Exact values must be preserved
PHASE_ACTION: Final[int] = 0      # Action selection
PHASE_EXPLORE: Final[int] = 1     # Explore phase
PHASE_DEVELOP: Final[int] = 2     # Develop phase
PHASE_SETTLE: Final[int] = 3      # Settle phase
PHASE_CONSUME: Final[int] = 4     # Consume phase
PHASE_PRODUCE: Final[int] = 5     # Produce phase
PHASE_DISCARD: Final[int] = 6     # Discard phase

# Action Choices - Exact values must be preserved
ACT_GAME_START: Final[int] = -2   # Game start special action
ACT_ROUND_START: Final[int] = -1  # Round start special action
ACT_SEARCH: Final[int] = 0        # Search action (expansions)
ACT_EXPLORE_5_0: Final[int] = 1   # Explore: Draw 5, keep 0
ACT_EXPLORE_1_1: Final[int] = 2   # Explore: Draw 1, keep 1
ACT_DEVELOP: Final[int] = 3       # Develop action
ACT_DEVELOP2: Final[int] = 4      # Advanced develop action
ACT_SETTLE: Final[int] = 5        # Settle action
ACT_SETTLE2: Final[int] = 6       # Advanced settle action
ACT_CONSUME_TRADE: Final[int] = 7 # Consume-trade action
ACT_CONSUME_X2: Final[int] = 8    # Consume-x2 action
ACT_PRODUCE: Final[int] = 9       # Produce action
ACT_ROUND_END: Final[int] = 10    # Round end special action

ACT_MASK: Final[int] = 0x7f       # Action mask
ACT_PRESTIGE: Final[int] = 0x80   # Prestige action flag

# Session Status Types - Must preserve exact values
SS_EMPTY: Final[int] = 0          # Empty session
SS_WAITING: Final[int] = 1        # Waiting for players
SS_STARTED: Final[int] = 2        # Game in progress
SS_DONE: Final[int] = 3           # Game completed
SS_ABANDONED: Final[int] = 4      # Game abandoned

# Power Types - Must match original exactly
P_DISCARD: Final[int] = 0         # Discard to use
P_CONSUME_HAND: Final[int] = 1    # Consume from hand
P_CONSUME_GOOD: Final[int] = 2    # Consume good
P_CONSUME_PRESTIGE: Final[int] = 3 # Consume prestige
P_TEMPORARY: Final[int] = 4       # Temporary power
P_GAME_START: Final[int] = 5      # Start of game
P_PREPARE: Final[int] = 6         # Phase preparation
P_START: Final[int] = 7           # Phase start
P_PLACE: Final[int] = 8           # Card placement
P_CONSUME_3_DIFF: Final[int] = 9  # Consume three different
P_CONSUME_N_DIFF: Final[int] = 10 # Consume N different
P_CONSUME_ALL: Final[int] = 11    # Consume all goods
P_PRODUCE: Final[int] = 12        # Production
P_PRODUCE_PRESTIGE: Final[int] = 13 # Produce prestige
P_VP: Final[int] = 14            # Victory points
P_TAKEOVER: Final[int] = 15      # Military takeover
P_END: Final[int] = 16           # End of game

# Choice Types for UI
CHOICE_ACTION: Final[int] = 0
CHOICE_START: Final[int] = 1
CHOICE_DISCARD: Final[int] = 2
CHOICE_SAVE: Final[int] = 3
CHOICE_DISCARD_PRESTIGE: Final[int] = 4
CHOICE_PLACE: Final[int] = 5
CHOICE_PAYMENT: Final[int] = 6
CHOICE_SETTLE: Final[int] = 7
CHOICE_TAKEOVER: Final[int] = 8
CHOICE_DEFEND: Final[int] = 9
CHOICE_UPGRADE: Final[int] = 10
CHOICE_TRADE: Final[int] = 11
CHOICE_CONSUME: Final[int] = 12
CHOICE_GOOD: Final[int] = 13
CHOICE_CONSUME_HAND: Final[int] = 14
CHOICE_ANTE: Final[int] = 15
CHOICE_KEEP: Final[int] = 16
CHOICE_WINDFALL: Final[int] = 17
CHOICE_PRODUCE: Final[int] = 18
CHOICE_DISCARD_HAND: Final[int] = 19
CHOICE_ORACLES: Final[int] = 20

# Expansion IDs
EXP_BASE: Final[int] = 0          # Base game only
EXP_TGS: Final[int] = 1           # The Gathering Storm
EXP_BOW: Final[int] = 2           # The Brink of War
EXP_AA: Final[int] = 3            # Alien Artifacts
EXP_XI: Final[int] = 4            # Xeno Invasion
EXP_RVI_ONLY: Final[int] = 5      # Rebel vs Imperium only
EXP_RVI: Final[int] = 6           # Rebel vs Imperium

# Network Message Types
MSG_LOGIN: Final[int] = 1         # Login request
MSG_HELLO: Final[int] = 2         # Server greeting
MSG_DENIED: Final[int] = 3        # Access denied
MSG_GOODBYE: Final[int] = 4       # Disconnect notification
MSG_PING: Final[int] = 5          # Keep-alive ping
MSG_PLAYER_NEW: Final[int] = 10   # New player joined
MSG_PLAYER_LEFT: Final[int] = 11  # Player disconnected
MSG_OPENGAME: Final[int] = 20     # Create new game
MSG_GAME_PLAYER: Final[int] = 21  # Player in game info
MSG_CLOSE_GAME: Final[int] = 22   # Close game
MSG_JOIN: Final[int] = 23         # Join request
MSG_LEAVE: Final[int] = 24        # Leave game
MSG_JOINACK: Final[int] = 25      # Join accepted
MSG_JOINNAK: Final[int] = 26      # Join rejected
MSG_CREATE: Final[int] = 27       # Create game
MSG_START: Final[int] = 28        # Start game
MSG_REMOVE: Final[int] = 29       # Remove player
MSG_RESIGN: Final[int] = 30       # Player resignation
MSG_ADD_AI: Final[int] = 31       # Add AI player
MSG_STATUS_META: Final[int] = 40  # Game metadata
MSG_STATUS_PLAYER: Final[int] = 41 # Player status
MSG_STATUS_CARD: Final[int] = 42  # Card status
MSG_STATUS_GOAL: Final[int] = 43  # Goal status
MSG_STATUS_MISC: Final[int] = 44  # Misc status
MSG_LOG: Final[int] = 45          # Game log
MSG_CHAT: Final[int] = 46         # Chat message
MSG_WAITING: Final[int] = 47      # Waiting notification
MSG_SEAT: Final[int] = 48         # Seat assignment
MSG_GAMECHAT: Final[int] = 49     # In-game chat
MSG_LOG_FORMAT: Final[int] = 50   # Log formatting
MSG_CHOOSE: Final[int] = 60       # Action choice
MSG_PREPARE: Final[int] = 61      # Prepare for choice
MSG_GAMEOVER: Final[int] = 70     # Game over

# Connection States
CS_EMPTY: Final[int] = 0          # No connection
CS_INIT: Final[int] = 1           # Initializing
CS_LOBBY: Final[int] = 2          # In lobby
CS_PLAYING: Final[int] = 3        # In game

# Buffer Sizes
BUF_LEN: Final[int] = 1024        # Message buffer length
HEADER_LEN: Final[int] = 8        # Message header length

# AI Constants
ROLE_HIDDEN: Final[int] = 50      # Hidden layer size
ROLE_OUT: Final[int] = 7          # Basic game outputs
ROLE_OUT_ADV: Final[int] = 23     # Advanced game outputs
ROLE_OUT_EXP3: Final[int] = 15    # Basic + Expansion 3 outputs
ROLE_OUT_ADV_EXP3: Final[int] = 76 # Advanced + Expansion 3 outputs

# Training Constants
PAST_MAX: Final[int] = 120        # Max previous inputs stored
