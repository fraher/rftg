"""
Test suite for the core game engine functionality.
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from core import GameEngine, GameState, Player, Card, Design, CardType, GoodType
from core.constants import *


class TestGameEngine:
    """Test the core game engine functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
    
    def test_engine_initialization(self):
        """Test that the engine initializes correctly."""
        assert self.engine is not None
        assert len(self.engine.designs) > 0
        assert self.engine.game is None
    
    def test_create_game(self):
        """Test game creation."""
        game = self.engine.create_game(num_players=2)
        
        assert game is not None
        assert game.num_players == 2
        assert len(game.players) == 2
        assert len(game.cards) > 0
        assert len(game.deck) > 0
        assert game.round == 1
        assert not game.game_over
    
    def test_create_game_invalid_players(self):
        """Test that invalid player counts are rejected."""
        with pytest.raises(ValueError):
            self.engine.create_game(num_players=1)
        
        with pytest.raises(ValueError):
            self.engine.create_game(num_players=7)
    
    def test_starting_hands(self):
        """Test that players get proper starting hands."""
        game = self.engine.create_game(num_players=2)
        
        for player in game.players:
            hand_size = player.get_hand_size(game.cards)
            assert hand_size == 6  # Standard starting hand size
    
    def test_starting_worlds(self):
        """Test that players get starting worlds."""
        game = self.engine.create_game(num_players=2)
        
        for player in game.players:
            assert player.start != -1
            start_card = game.cards[player.start]
            assert start_card.design.is_start_world
            assert start_card.owner == game.players.index(player)
    
    def test_deck_shuffle(self):
        """Test that the deck is shuffled."""
        # Create two games with different seeds
        game1 = self.engine.create_game(num_players=2, seed=12345)
        engine2 = GameEngine()
        game2 = engine2.create_game(num_players=2, seed=54321)
        
        # Decks should be in different order (very high probability)
        assert game1.deck != game2.deck


class TestGameState:
    """Test the game state data structures."""
    
    def test_player_initialization(self):
        """Test player initialization."""
        player = Player(name="Test Player")
        
        assert player.name == "Test Player"
        assert not player.ai
        assert player.vp == 0
        assert player.prestige == 0
        assert len(player.head) == MAX_WHERE
        assert all(head == -1 for head in player.head)
    
    def test_card_creation(self):
        """Test card creation from design."""
        design = Design(
            index=0,
            name="Test Card",
            type=CardType.WORLD,
            cost=2,
            vp=1,
            flags=0,
            good_type=GoodType.NOVELTY
        )
        
        card = Card(design=design)
        
        assert card.name == "Test Card"
        assert card.type == CardType.WORLD
        assert card.cost == 2
        assert card.vp == 1
        assert card.good_type == GoodType.NOVELTY
        assert card.owner == -1
        assert card.where.value == WHERE_DECK
    
    def test_card_flag_checking(self):
        """Test card flag checking."""
        design = Design(
            index=0,
            name="Military World",
            type=CardType.WORLD,
            cost=2,
            vp=2,
            flags=FLAG_MILITARY | FLAG_WINDFALL,
            good_type=GoodType.ALIEN
        )
        
        card = Card(design=design)
        
        assert card.has_flag(FLAG_MILITARY)
        assert card.has_flag(FLAG_WINDFALL)
        assert not card.has_flag(FLAG_START)
    
    def test_game_state_initialization(self):
        """Test game state initialization."""
        game = GameState(num_players=3)
        
        assert game.num_players == 3
        assert len(game.players) == 3
        assert game.round == 0
        assert not game.game_over
        assert len(game.goal_avail) == MAX_GOAL


class TestGameMechanics:
    """Test specific game mechanics."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = GameEngine()
        self.game = self.engine.create_game(num_players=2)
    
    def test_draw_card(self):
        """Test drawing cards from deck."""
        initial_deck_size = len(self.game.deck)
        
        card_idx = self.game.draw_card()
        
        assert card_idx is not None
        assert len(self.game.deck) == initial_deck_size - 1
    
    def test_add_card_to_hand(self):
        """Test adding cards to player's hand."""
        player_idx = 0
        card_idx = self.game.draw_card()
        
        initial_hand_size = self.game.players[player_idx].get_hand_size(self.game.cards)
        
        self.game.add_card_to_hand(player_idx, card_idx)
        
        new_hand_size = self.game.players[player_idx].get_hand_size(self.game.cards)
        assert new_hand_size == initial_hand_size + 1
        
        card = self.game.cards[card_idx]
        assert card.owner == player_idx
        assert card.where.value == WHERE_HAND
    
    def test_calculate_vp(self):
        """Test victory point calculation."""
        player_idx = 0
        
        # Initial VP should be from starting world
        vp = self.game.calculate_vp(player_idx)
        assert vp > 0  # Should have VP from starting world
    
    def test_military_strength(self):
        """Test military strength calculation."""
        player = self.game.players[0]
        
        # Should have base military strength (may be 0 for non-military starts)
        military = player.get_military_strength(self.game.cards)
        assert military >= 0
    
    def test_action_selection(self):
        """Test action selection mechanism."""
        actions = [[ACT_EXPLORE_1_1, 0], [ACT_DEVELOP, 0]]
        
        self.engine.select_actions(actions)
        
        assert self.game.players[0].action[0] == ACT_EXPLORE_1_1
        assert self.game.players[1].action[0] == ACT_DEVELOP
        
        # Check that active phases are determined
        active_phases = self.game.options.get('active_phases', [])
        assert ACT_EXPLORE_1_1 in active_phases
        assert ACT_DEVELOP in active_phases


if __name__ == "__main__":
    pytest.main([__file__])
