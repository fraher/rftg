"""
Race for the Galaxy - Python Implementation

This is the main package for the Python implementation of Race for the Galaxy.
"""

from .core import GameEngine, GameState, VERSION

__version__ = VERSION
__author__ = "Race for the Galaxy Python Team"
__email__ = ""
__description__ = "Python implementation of Race for the Galaxy"

def main():
    """Main entry point for the application."""
    print(f"Race for the Galaxy Python Implementation v{VERSION}")
    print("Loading game engine...")
    
    # Create and initialize game engine
    engine = GameEngine()
    
    # For now, just create a test game
    print("Creating test game...")
    game = engine.create_game(num_players=2)
    
    print(f"Game created with {game.num_players} players")
    print(f"Deck size: {len(game.deck)} cards")
    print(f"Total cards: {len(game.cards)} cards")
    
    # Show player hand sizes
    for i, player in enumerate(game.players):
        hand_size = player.get_hand_size(game.cards)
        print(f"Player {i+1} ({player.name}): {hand_size} cards in hand")
    
    print("Game initialization complete!")

if __name__ == "__main__":
    main()
