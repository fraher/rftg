"""
Core data types for Race for the Galaxy

This module defines the fundamental data structures that correspond exactly
to the C implementation, ensuring perfect compatibility.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import IntEnum
import numpy as np

from .constants import *


class CardType(IntEnum):
    """Card type enumeration matching C implementation."""
    WORLD = 1
    DEVELOPMENT = 2


class GoodType(IntEnum):
    """Good type enumeration."""
    NONE = 0
    ANY = GOOD_ANY
    NOVELTY = GOOD_NOVELTY
    RARE = GOOD_RARE
    GENE = GOOD_GENE
    ALIEN = GOOD_ALIEN


class CardLocation(IntEnum):
    """Card location enumeration."""
    DECK = WHERE_DECK
    DISCARD = WHERE_DISCARD
    HAND = WHERE_HAND
    ACTIVE = WHERE_ACTIVE
    GOOD = WHERE_GOOD
    VP = WHERE_VP
    SAVED = WHERE_SAVED
    PRESTIGE = WHERE_PRESTIGE


class GamePhase(IntEnum):
    """Game phase enumeration."""
    ACTION = PHASE_ACTION
    EXPLORE = PHASE_EXPLORE
    DEVELOP = PHASE_DEVELOP
    SETTLE = PHASE_SETTLE
    CONSUME = PHASE_CONSUME
    PRODUCE = PHASE_PRODUCE
    DISCARD = PHASE_DISCARD


class ActionChoice(IntEnum):
    """Action choice enumeration."""
    GAME_START = ACT_GAME_START
    ROUND_START = ACT_ROUND_START
    SEARCH = ACT_SEARCH
    EXPLORE_5_0 = ACT_EXPLORE_5_0
    EXPLORE_1_1 = ACT_EXPLORE_1_1
    DEVELOP = ACT_DEVELOP
    DEVELOP2 = ACT_DEVELOP2
    SETTLE = ACT_SETTLE
    SETTLE2 = ACT_SETTLE2
    CONSUME_TRADE = ACT_CONSUME_TRADE
    CONSUME_X2 = ACT_CONSUME_X2
    PRODUCE = ACT_PRODUCE
    ROUND_END = ACT_ROUND_END


class PowerType(IntEnum):
    """Power type enumeration."""
    DISCARD = P_DISCARD
    CONSUME_HAND = P_CONSUME_HAND
    CONSUME_GOOD = P_CONSUME_GOOD
    CONSUME_PRESTIGE = P_CONSUME_PRESTIGE
    TEMPORARY = P_TEMPORARY
    GAME_START = P_GAME_START
    PREPARE = P_PREPARE
    START = P_START
    PLACE = P_PLACE
    CONSUME_3_DIFF = P_CONSUME_3_DIFF
    CONSUME_N_DIFF = P_CONSUME_N_DIFF
    CONSUME_ALL = P_CONSUME_ALL
    PRODUCE = P_PRODUCE
    PRODUCE_PRESTIGE = P_PRODUCE_PRESTIGE
    VP = P_VP
    TAKEOVER = P_TAKEOVER
    END = P_END


@dataclass
class Power:
    """
    Card power definition matching the C implementation.
    
    This represents a single power on a card, with all the necessary
    data to determine when and how it activates.
    """
    type: PowerType
    code: int
    value: int
    times: int
    
    def __post_init__(self):
        """Validate power data after initialization."""
        if not isinstance(self.type, PowerType):
            self.type = PowerType(self.type)


@dataclass
class VPBonus:
    """
    Victory point bonus structure.
    
    Represents special victory point calculations for 6-cost developments
    and other cards with complex scoring.
    """
    type: int
    value: int
    name: str


@dataclass
class Design:
    """
    Card design definition matching the C implementation.
    
    This contains all the static information about a card design,
    separate from the runtime card instance data.
    """
    index: int                          # Card design index
    name: str                          # Card name
    type: CardType                     # World or Development
    cost: int                          # Base cost (0-6)
    vp: int                           # Victory points
    flags: int                        # Card flags (64-bit)
    good_type: GoodType               # Type of good produced
    powers: List[Power] = field(default_factory=list)  # Powers on card
    vp_bonuses: List[VPBonus] = field(default_factory=list)  # VP bonuses
    
    def __post_init__(self):
        """Validate design data after initialization."""
        if not isinstance(self.type, CardType):
            self.type = CardType(self.type)
        if not isinstance(self.good_type, GoodType):
            self.good_type = GoodType(self.good_type)
        
        # Validate powers
        for i, power in enumerate(self.powers):
            if not isinstance(power, Power):
                self.powers[i] = Power(**power)
    
    @property
    def is_world(self) -> bool:
        """Check if this is a world card."""
        return self.type == CardType.WORLD
    
    @property
    def is_development(self) -> bool:
        """Check if this is a development card."""
        return self.type == CardType.DEVELOPMENT
    
    @property
    def is_military(self) -> bool:
        """Check if this is a military world."""
        return bool(self.flags & FLAG_MILITARY)
    
    @property
    def is_windfall(self) -> bool:
        """Check if this is a windfall world."""
        return bool(self.flags & FLAG_WINDFALL)
    
    @property
    def is_start_world(self) -> bool:
        """Check if this is a starting world."""
        return bool(self.flags & FLAG_START)


@dataclass
class Card:
    """
    Runtime card instance matching the C implementation.
    
    This represents a specific card instance in the game, with runtime
    state like location, owner, and goods placed on it.
    """
    design: Design                     # Reference to card design
    owner: int = -1                   # Player who owns this card (-1 = none)
    where: CardLocation = CardLocation.DECK  # Current location
    start_owner: int = -1             # Owner at start of phase
    start_where: CardLocation = CardLocation.DECK  # Location at start of phase
    misc: int = 0                     # Miscellaneous flags
    covering: int = -1                # Card this good is covering (-1 = none)
    num_goods: int = 0                # Number of goods on this card
    order: int = 0                    # Order played on table
    next: int = -1                    # Next card in owner's list (-1 = end)
    start_next: int = -1              # Next card at start of phase
    
    def __post_init__(self):
        """Validate card data after initialization."""
        if not isinstance(self.where, CardLocation):
            self.where = CardLocation(self.where)
        if not isinstance(self.start_where, CardLocation):
            self.start_where = CardLocation(self.start_where)
    
    @property
    def index(self) -> int:
        """Get the design index of this card."""
        return self.design.index
    
    @property
    def name(self) -> str:
        """Get the name of this card."""
        return self.design.name
    
    @property
    def type(self) -> CardType:
        """Get the type of this card."""
        return self.design.type
    
    @property
    def cost(self) -> int:
        """Get the cost of this card."""
        return self.design.cost
    
    @property
    def vp(self) -> int:
        """Get the VP value of this card."""
        return self.design.vp
    
    @property
    def flags(self) -> int:
        """Get the flags of this card."""
        return self.design.flags
    
    @property
    def good_type(self) -> GoodType:
        """Get the good type of this card."""
        return self.design.good_type
    
    @property
    def powers(self) -> List[Power]:
        """Get the powers of this card."""
        return self.design.powers
    
    def has_flag(self, flag: int) -> bool:
        """Check if this card has a specific flag."""
        return bool(self.flags & flag)
    
    def is_active(self) -> bool:
        """Check if this card is in a player's tableau."""
        return self.where == CardLocation.ACTIVE
    
    def is_good(self) -> bool:
        """Check if this card is being used as a good."""
        return self.where == CardLocation.GOOD
    
    def can_produce_good(self) -> bool:
        """Check if this card can produce a good."""
        return (self.design.good_type != GoodType.NONE and 
                not self.has_flag(FLAG_NO_PRODUCE) and
                self.is_active())


@dataclass
class Player:
    """
    Player state matching the C implementation.
    
    Contains all the information about a player's current state,
    including cards, scores, and temporary state.
    """
    name: str                         # Player name/color
    ai: bool = False                 # Whether played by AI
    
    # Actions
    action: List[int] = field(default_factory=lambda: [0, 0])  # Chosen actions
    prev_action: List[int] = field(default_factory=lambda: [0, 0])  # Previous actions
    prestige_action_used: bool = False  # Used prestige action this round
    phase_bonus_used: bool = False   # Used phase bonus this round
    
    # Cards
    start: int = -1                  # Start world card index
    head: List[int] = field(default_factory=lambda: [-1] * MAX_WHERE)  # First card in each location
    start_head: List[int] = field(default_factory=lambda: [-1] * MAX_WHERE)  # At start of phase
    placing: int = -1                # Card being placed this phase
    
    # Temporary bonuses
    bonus_military: int = 0          # Bonus military this phase
    bonus_military_xeno: int = 0     # Bonus military vs Xeno this phase
    bonus_reduce: int = 0            # Bonus settle discount this phase
    hand_military_spent: int = 0     # Hand military spent this phase
    military_spent: int = 0          # Total military spent this phase
    end_discard: int = 0             # Cards to discard at end of turn
    
    # Goals and scoring
    goal_claimed: List[bool] = field(default_factory=lambda: [False] * MAX_GOAL)  # Goals claimed
    goal_progress: List[int] = field(default_factory=lambda: [0] * MAX_GOAL)  # Progress toward goals
    prestige: int = 0                # Prestige points
    prestige_turn: int = 0           # Prestige earned this turn
    vp: int = 0                     # Victory point chips
    goal_vp: int = 0                # Victory points from goals
    end_vp: int = 0                 # Total VP if game ended now
    winner: bool = False            # Is the winner
    
    # Simulation state
    fake_hand: int = 0              # Fake drawn cards in simulation
    fake_discards: int = 0          # Fake discarded cards
    drawn_round: int = 0            # Cards drawn this round
    skip_develop: bool = False      # Skipped last develop phase
    skip_settle: bool = False       # Skipped last settle phase
    low_hand: int = 0              # Lowest hand size this turn
    table_order: int = 0           # Counter for card play order
    
    # Phase tracking
    phase_cards: int = 0           # Cards gained this phase
    phase_vp: int = 0              # VP gained this phase
    phase_prestige: int = 0        # Prestige gained this phase
    
    # Choice logging
    choice_log: List[int] = field(default_factory=list)  # Log of choices
    choice_size: int = 0           # Size of choice log
    choice_pos: int = 0            # Current position in log
    choice_history: List[int] = field(default_factory=list)  # History of log sizes
    choice_unread_pos: int = 0     # Last unread position
    
    def get_hand_size(self, cards: List[Card]) -> int:
        """Count cards in player's hand."""
        count = 0
        current = self.head[WHERE_HAND]
        while current != -1:
            count += 1
            current = cards[current].next
        return count
    
    def get_active_cards(self, cards: List[Card]) -> List[int]:
        """Get list of cards in player's tableau."""
        result = []
        current = self.head[WHERE_ACTIVE]
        while current != -1:
            result.append(current)
            current = cards[current].next
        return result
    
    def get_military_strength(self, cards: List[Card]) -> int:
        """Calculate total military strength."""
        military = self.bonus_military
        
        # Add military from active cards
        for card_idx in self.get_active_cards(cards):
            card = cards[card_idx]
            if card.has_flag(FLAG_MILITARY):
                military += 1  # Base military for military worlds
                # TODO: Add military from powers
        
        return military
    
    def can_afford_card(self, card_design: Design, cards: List[Card]) -> bool:
        """Check if player can afford to play a card."""
        cost = card_design.cost
        
        # Apply discounts
        cost -= self.bonus_reduce
        
        # Military worlds use military instead of cost
        if card_design.is_military:
            return self.get_military_strength(cards) >= cost
        
        # Regular worlds/developments use cards from hand
        hand_size = self.get_hand_size(cards)
        return hand_size >= cost


@dataclass
class GameState:
    """
    Complete game state matching the C implementation.
    
    This contains all information needed to represent the current
    state of a game, including all cards, players, and game settings.
    """
    # Game setup
    num_players: int = 2            # Number of players
    expanded: int = 0               # Expansion level
    advanced: bool = False          # Advanced game flag
    goal_disabled: bool = False     # Goals disabled
    takeover_disabled: bool = False # Takeovers disabled
    campaign_name: str = "none"     # Campaign name
    
    # Game state
    session_id: int = 0             # Session ID for networking
    round: int = 0                  # Current round number
    cur_action: ActionChoice = ActionChoice.ROUND_START  # Current action/phase
    turn: int = 0                   # Current player's turn
    game_over: bool = False         # Game is finished
    
    # Random number generation
    seed: int = 0                   # Current RNG seed
    random_state: Optional[np.random.RandomState] = None  # RNG state
    
    # Cards
    designs: List[Design] = field(default_factory=list)  # All card designs
    cards: List[Card] = field(default_factory=list)      # All card instances
    deck: List[int] = field(default_factory=list)        # Deck card indices
    discard: List[int] = field(default_factory=list)     # Discard pile
    
    # Players
    players: List[Player] = field(default_factory=list)  # All players
    
    # Goals and achievements
    goals: List[Dict[str, Any]] = field(default_factory=list)  # Goal definitions
    goal_avail: List[bool] = field(default_factory=list)  # Available goals
    
    # Game options
    options: Dict[str, Any] = field(default_factory=dict)  # Game options
    
    def __post_init__(self):
        """Initialize game state after creation."""
        if self.random_state is None:
            self.random_state = np.random.RandomState(self.seed)
        
        # Ensure we have the right number of players
        while len(self.players) < self.num_players:
            self.players.append(Player(name=f"Player {len(self.players) + 1}"))
        
        # Initialize goals list
        if not self.goal_avail:
            self.goal_avail = [True] * MAX_GOAL
    
    def get_current_player(self) -> Player:
        """Get the current active player."""
        return self.players[self.turn]
    
    def next_turn(self) -> None:
        """Advance to the next player's turn."""
        self.turn = (self.turn + 1) % self.num_players
    
    def is_action_selected(self, action: ActionChoice) -> bool:
        """Check if any player selected the given action."""
        for player in self.players:
            if action in player.action:
                return True
        return False
    
    def get_players_with_action(self, action: ActionChoice) -> List[int]:
        """Get list of player indices who selected the given action."""
        result = []
        for i, player in enumerate(self.players):
            if action in player.action:
                result.append(i)
        return result
    
    def shuffle_deck(self) -> None:
        """Shuffle the deck using the game's RNG."""
        if self.random_state is not None:
            self.random_state.shuffle(self.deck)
    
    def draw_card(self) -> Optional[int]:
        """Draw a card from the deck."""
        if not self.deck:
            # Reshuffle discard pile if deck is empty
            if self.discard:
                self.deck = self.discard.copy()
                self.discard.clear()
                self.shuffle_deck()
            else:
                return None
        
        return self.deck.pop() if self.deck else None
    
    def add_card_to_hand(self, player_idx: int, card_idx: int) -> None:
        """Add a card to a player's hand."""
        card = self.cards[card_idx]
        player = self.players[player_idx]
        
        # Update card state
        card.owner = player_idx
        card.where = CardLocation.HAND
        
        # Add to player's hand list
        card.next = player.head[WHERE_HAND]
        player.head[WHERE_HAND] = card_idx
    
    def remove_card_from_location(self, player_idx: int, card_idx: int, location: CardLocation) -> None:
        """Remove a card from a specific location in a player's card lists."""
        player = self.players[player_idx]
        card = self.cards[card_idx]
        
        # Find and remove from linked list
        if player.head[location] == card_idx:
            player.head[location] = card.next
        else:
            # Find previous card in list
            current = player.head[location]
            while current != -1 and self.cards[current].next != card_idx:
                current = self.cards[current].next
            
            if current != -1:
                self.cards[current].next = card.next
        
        card.next = -1
    
    def calculate_vp(self, player_idx: int) -> int:
        """Calculate total victory points for a player."""
        player = self.players[player_idx]
        total_vp = player.vp + player.goal_vp
        
        # Add VP from active cards
        for card_idx in player.get_active_cards(self.cards):
            card = self.cards[card_idx]
            total_vp += card.vp
            
            # TODO: Add VP from card powers and bonuses
        
        return total_vp
    
    def check_game_end(self) -> bool:
        """Check if the game should end."""
        for player in self.players:
            # Check for 12+ cards in tableau
            active_count = len(player.get_active_cards(self.cards))
            if active_count >= 12:
                return True
            
            # Check for 14+ VP (if special flag is set)
            if self.calculate_vp(self.players.index(player)) >= 14:
                # TODO: Check for FLAG_GAME_END_14
                pass
        
        # Check if deck and discard are both empty
        if not self.deck and not self.discard:
            return True
        
        return False
