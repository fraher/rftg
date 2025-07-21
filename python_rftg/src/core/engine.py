"""
Core game engine for Race for the Galaxy

This module implements the main game logic, including initialization,
phase execution, and game flow control.
"""

from typing import List, Optional, Dict, Any, Tuple
import json
import os
from pathlib import Path

from .constants import *
from .game_state import GameState, Player, Card, Design, Power, VPBonus, CardType, GoodType, PowerType, CardLocation, ActionChoice


class GameEngine:
    """
    Core game engine implementing Race for the Galaxy game logic.
    
    This class manages the complete game state and provides methods for
    initializing games, executing phases, and handling player actions.
    """
    
    def __init__(self):
        """Initialize the game engine."""
        self.game: Optional[GameState] = None
        self.designs: List[Design] = []
        self._load_card_designs()
    
    def _load_card_designs(self) -> None:
        """Load card designs from data files."""
        # For now, create some basic test cards
        # TODO: Load from actual card data files
        self.designs = self._create_test_cards()
    
    def _create_test_cards(self) -> List[Design]:
        """Create a minimal set of test cards for development."""
        designs = []
        
        # Starting worlds
        designs.append(Design(
            index=0,
            name="Old Earth",
            type=CardType.WORLD,
            cost=0,
            vp=1,
            flags=FLAG_START,
            good_type=GoodType.NONE,
            powers=[]
        ))
        
        designs.append(Design(
            index=1,
            name="Epsilon Eridani",
            type=CardType.WORLD,
            cost=1,
            vp=1,
            flags=FLAG_START,
            good_type=GoodType.RARE,
            powers=[]
        ))
        
        # Basic development
        designs.append(Design(
            index=2,
            name="Contact Specialist",
            type=CardType.DEVELOPMENT,
            cost=1,
            vp=0,
            flags=0,
            good_type=GoodType.NONE,
            powers=[Power(type=P_VP, code=0, value=1, times=1)]
        ))
        
        # Basic world
        designs.append(Design(
            index=3,
            name="Alpha Centauri",
            type=CardType.WORLD,
            cost=1,
            vp=1,
            flags=0,
            good_type=GoodType.NOVELTY,
            powers=[]
        ))
        
        # Military world
        designs.append(Design(
            index=4,
            name="Damaged Alien Factory",
            type=CardType.WORLD,
            cost=1,
            vp=2,
            flags=FLAG_MILITARY,
            good_type=GoodType.ALIEN,
            powers=[]
        ))
        
        # Add more non-starting cards for testing
        for i in range(5, 25):  # Create 20 more cards
            if i % 2 == 0:  # Even numbers = developments
                designs.append(Design(
                    index=i,
                    name=f"Development {i}",
                    type=CardType.DEVELOPMENT,
                    cost=(i % 6) + 1,  # Cost 1-6
                    vp=i % 3,  # VP 0-2
                    flags=0,
                    good_type=GoodType.NONE,
                    powers=[]
                ))
            else:  # Odd numbers = worlds
                designs.append(Design(
                    index=i,
                    name=f"World {i}",
                    type=CardType.WORLD,
                    cost=(i % 6) + 1,  # Cost 1-6
                    vp=(i % 3) + 1,  # VP 1-3
                    flags=0,
                    good_type=GoodType((i % 4) + 2),  # Rotating good types
                    powers=[]
                ))
        
        return designs
    
    def create_game(self, num_players: int = 2, **options) -> GameState:
        """
        Create a new game with the specified number of players.
        
        Args:
            num_players: Number of players (2-6)
            **options: Additional game options
        
        Returns:
            Newly created game state
        """
        if not (2 <= num_players <= MAX_PLAYER):
            raise ValueError(f"Number of players must be between 2 and {MAX_PLAYER}")
        
        # Create game state
        self.game = GameState(
            num_players=num_players,
            designs=self.designs.copy(),
            **options
        )
        
        # Initialize RNG
        if 'seed' in options:
            self.game.seed = options['seed']
        else:
            import time
            self.game.seed = int(time.time()) & 0xFFFFFFFF
        
        import numpy as np
        self.game.random_state = np.random.RandomState(self.game.seed)
        
        # Create card instances
        self._initialize_cards()
        
        # Set up players
        self._initialize_players()
        
        # Deal starting hands
        self._deal_starting_game()
        
        return self.game
    
    def _initialize_cards(self) -> None:
        """Create card instances from designs."""
        if not self.game:
            raise RuntimeError("No game created")
        
        self.game.cards = []
        self.game.deck = []
        
        # Create cards for each design
        for design in self.game.designs:
            # Most cards have only one copy, but some may have multiple
            num_copies = 1
            
            for copy_num in range(num_copies):
                card_idx = len(self.game.cards)
                card = Card(design=design)
                self.game.cards.append(card)
                
                # Add non-starting cards to deck
                if not design.is_start_world:
                    self.game.deck.append(card_idx)
        
        # Shuffle the deck
        self.game.shuffle_deck()
    
    def _initialize_players(self) -> None:
        """Initialize player states."""
        if not self.game:
            raise RuntimeError("No game created")
        
        # Create players if needed
        while len(self.game.players) < self.game.num_players:
            player_idx = len(self.game.players)
            player = Player(name=f"Player {player_idx + 1}")
            self.game.players.append(player)
        
        # Assign starting worlds
        start_worlds = [card for card in self.game.cards 
                       if card.design.is_start_world]
        
        for i, player in enumerate(self.game.players):
            if i < len(start_worlds):
                card_idx = self.game.cards.index(start_worlds[i])
                player.start = card_idx
                
                # Place starting world in tableau
                card = self.game.cards[card_idx]
                card.owner = i
                card.where = CardLocation.ACTIVE
                player.head[WHERE_ACTIVE] = card_idx
    
    def _deal_starting_game(self) -> None:
        """Deal starting hands and set up initial game state."""
        if not self.game:
            raise RuntimeError("No game created")
        
        # Deal starting hands (6 cards each in base game)
        starting_hand_size = 6
        
        for player_idx, player in enumerate(self.game.players):
            for _ in range(starting_hand_size):
                card_idx = self.game.draw_card()
                if card_idx is not None:
                    self.game.add_card_to_hand(player_idx, card_idx)
        
        # Set initial game state
        self.game.round = 1
        self.game.turn = 0
        self.game.cur_action = ActionChoice.ROUND_START
    
    def start_round(self) -> None:
        """Start a new round of the game."""
        if not self.game:
            raise RuntimeError("No game created")
        
        # Reset player states for new round
        for player in self.game.players:
            player.action = [0, 0]
            player.prestige_action_used = False
            player.phase_bonus_used = False
            player.bonus_military = 0
            player.bonus_military_xeno = 0
            player.bonus_reduce = 0
            player.hand_military_spent = 0
            player.military_spent = 0
            player.placing = -1
        
        # Advance to action selection phase
        self.game.cur_action = ActionChoice.ROUND_START
    
    def select_actions(self, actions: List[List[int]]) -> None:
        """
        Have players select their actions for the round.
        
        Args:
            actions: List of action choices for each player
        """
        if not self.game:
            raise RuntimeError("No game created")
        
        if len(actions) != self.game.num_players:
            raise ValueError("Must provide actions for all players")
        
        # Store player action choices
        for i, player_actions in enumerate(actions):
            player = self.game.players[i]
            player.action = player_actions[:2]  # Max 2 actions
            
        # Determine which phases will be executed
        self._determine_active_phases()
    
    def _determine_active_phases(self) -> None:
        """Determine which phases will be executed based on player actions."""
        if not self.game:
            raise RuntimeError("No game created")
        
        # Check which actions were selected
        selected_actions = set()
        for player in self.game.players:
            for action in player.action:
                if action > 0:
                    selected_actions.add(action)
        
        # Store active phases for this round
        self.game.options['active_phases'] = list(selected_actions)
    
    def execute_round(self) -> None:
        """Execute all phases of the current round."""
        if not self.game:
            raise RuntimeError("No game created")
        
        active_phases = self.game.options.get('active_phases', [])
        
        # Execute phases in order
        for phase in sorted(active_phases):
            if phase == ACT_EXPLORE_5_0 or phase == ACT_EXPLORE_1_1:
                self._execute_explore_phase(phase)
            elif phase == ACT_DEVELOP or phase == ACT_DEVELOP2:
                self._execute_develop_phase(phase)
            elif phase == ACT_SETTLE or phase == ACT_SETTLE2:
                self._execute_settle_phase(phase)
            elif phase == ACT_CONSUME_TRADE or phase == ACT_CONSUME_X2:
                self._execute_consume_phase(phase)
            elif phase == ACT_PRODUCE:
                self._execute_produce_phase()
        
        # End of round cleanup
        self._end_round()
    
    def _execute_explore_phase(self, action: int) -> None:
        """Execute the explore phase."""
        if not self.game:
            return
        
        # Determine draw/keep amounts
        if action == ACT_EXPLORE_5_0:
            draw_amount = 5
            keep_amount = 1  # Actually keep 1, discard 4
        else:  # ACT_EXPLORE_1_1
            draw_amount = 2
            keep_amount = 1
        
        # Each player who selected this action draws and keeps cards
        for player_idx, player in enumerate(self.game.players):
            if action in player.action:
                # Draw cards
                drawn_cards = []
                for _ in range(draw_amount):
                    card_idx = self.game.draw_card()
                    if card_idx is not None:
                        drawn_cards.append(card_idx)
                
                # For now, just keep the first card and discard the rest
                # TODO: Implement proper player choice mechanism
                if drawn_cards:
                    # Keep first card
                    self.game.add_card_to_hand(player_idx, drawn_cards[0])
                    
                    # Discard the rest
                    for card_idx in drawn_cards[1:]:
                        self.game.discard.append(card_idx)
                        self.game.cards[card_idx].where = CardLocation.DISCARD
    
    def _execute_develop_phase(self, action: int) -> None:
        """Execute the develop phase."""
        if not self.game:
            return
        
        # Players who selected this action can play developments
        for player_idx, player in enumerate(self.game.players):
            if action in player.action:
                # TODO: Implement development placement
                # For now, just a placeholder
                pass
    
    def _execute_settle_phase(self, action: int) -> None:
        """Execute the settle phase."""
        if not self.game:
            return
        
        # Players who selected this action can play worlds
        for player_idx, player in enumerate(self.game.players):
            if action in player.action:
                # TODO: Implement world settlement
                # For now, just a placeholder
                pass
    
    def _execute_consume_phase(self, action: int) -> None:
        """Execute the consume phase."""
        if not self.game:
            return
        
        # TODO: Implement consume logic
        pass
    
    def _execute_produce_phase(self) -> None:
        """Execute the produce phase."""
        if not self.game:
            return
        
        # All players produce goods on eligible worlds
        for player_idx, player in enumerate(self.game.players):
            for card_idx in player.get_active_cards(self.game.cards):
                card = self.game.cards[card_idx]
                if card.can_produce_good() and card.num_goods == 0:
                    # Place a good on the card
                    card.num_goods = 1
                    # TODO: Handle windfall vs non-windfall production
    
    def _end_round(self) -> None:
        """Clean up at the end of a round."""
        if not self.game:
            return
        
        # Check for game end conditions
        if self.game.check_game_end():
            self._end_game()
            return
        
        # Advance to next round
        self.game.round += 1
        self.start_round()
    
    def _end_game(self) -> None:
        """End the game and determine winner."""
        if not self.game:
            return
        
        self.game.game_over = True
        
        # Calculate final scores
        final_scores = []
        for player_idx, player in enumerate(self.game.players):
            score = self.game.calculate_vp(player_idx)
            final_scores.append((score, player_idx))
        
        # Determine winner (highest score)
        final_scores.sort(reverse=True)
        winner_idx = final_scores[0][1]
        self.game.players[winner_idx].winner = True
    
    def get_game_state(self) -> Optional[GameState]:
        """Get the current game state."""
        return self.game
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game is not None and self.game.game_over
    
    def get_winner(self) -> Optional[int]:
        """Get the index of the winning player, or None if game not over."""
        if not self.is_game_over():
            return None
        
        for i, player in enumerate(self.game.players):
            if player.winner:
                return i
        
        return None
    
    def get_player_scores(self) -> List[int]:
        """Get the current scores for all players."""
        if not self.game:
            return []
        
        return [self.game.calculate_vp(i) for i in range(self.game.num_players)]
    
    def save_game(self, filename: str) -> None:
        """Save the current game state to a file."""
        if not self.game:
            raise RuntimeError("No game to save")
        
        # TODO: Implement proper save format matching C implementation
        # For now, just use JSON for development
        game_data = {
            'version': VERSION,
            'seed': self.game.seed,
            'round': self.game.round,
            'num_players': self.game.num_players,
            # TODO: Add complete game state serialization
        }
        
        with open(filename, 'w') as f:
            json.dump(game_data, f, indent=2)
    
    def load_game(self, filename: str) -> GameState:
        """Load a game state from a file."""
        with open(filename, 'r') as f:
            game_data = json.load(f)
        
        # TODO: Implement proper load format matching C implementation
        # For now, just create a new game with saved parameters
        self.game = self.create_game(
            num_players=game_data['num_players'],
            seed=game_data['seed']
        )
        
        return self.game
