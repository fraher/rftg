# Race for the Galaxy Implementation Specifications

This document provides comprehensive technical specifications for the Race for the Galaxy digital implementation. It serves as the authoritative reference for ensuring perfect compatibility with version 0.9.5 of Keldon Jones' implementation, including all modifications by B. Nordli and J.-R. Reinhard.

## Document Control
- Version: 1.0
- Last Updated: July 18, 2025
- Original Version: 0.9.5
- Original Source: Keldon Jones' C Implementation (2009-2015)
  - Modified by B. Nordli (October 2016)
  - Modified by J.-R. Reinhard (November 2016)
- License: GNU General Public License, version 2 (GPLv2)
- Original Release Date: 2009
- Last Source Update: April 2017

## System Constants
```c
// Critical game constants that must be preserved exactly
#define MAX_PLAYER 6        // Maximum number of players
#define AVAILABLE_DESIGN 300 // Available card design slots
#define MAX_DESIGN 280      // Original card designs
#define MAX_DECK 328        // Cards in deck
#define MAX_POWER 5         // Powers per card
#define MAX_VP_BONUS 6      // Special VP bonuses per card
#define MAX_TAKEOVER 12     // Maximum pending takeovers

// Version compatibility
#define VERSION "0.9.5"     // Current version
#define COMM_VERSION "0.9.4" // Minimum compatible server version

## Overview

### Purpose
This specification documents every aspect of the Race for the Galaxy digital implementation, ensuring perfect compatibility with the original while enabling future maintainability and potential enhancements.

### Scope
- Complete game rules implementation
- User interface and visual presentation
- AI system and neural network
- Networking protocol
- Data formats and persistence
- Cross-platform compatibility
- Expansion content integration

### Reference Materials
- Original C source code by Keldon Jones
- Race for the Galaxy board game rules
- Rio Grande Games official documentation
- Original AI training data and networks
- Campaign mode scenarios
- Expansion rule sets

## Client Configuration

### User Options
```c
typedef struct options {
    // Game settings
    int num_players;        // Number of players (default: 3)
    int expanded;           // Expansion level
    char *player_name;      // Player name
    int advanced;           // Two-player advanced game
    int promo;             // Use promo cards
    int disable_goal;      // Goals disabled
    int disable_takeover;  // Takeovers disabled
    
    // Custom game settings
    int customize_seed;    // Use custom seed
    unsigned int seed;     // Custom seed value
    char *campaign_name;   // Campaign name
    
    // Display options
    int hide_card;         // Hide card preview (0:Show, 2:Hide)
    int full_reduced;      // Reduce full-size card image
    int shrink_opponent;   // Shrink opponent areas
    int settle_discount;   // Show settle discount icon
    int vp_in_hand;       // Show VP for cards in hand
    int cost_in_hand;     // Show cost during placement
    int key_cues;         // Always show key cues
    int auto_select;      // Auto-select forced choices
    int card_size;        // Card display size
    int log_width;        // Log window width
    
    // Network options
    char *server_name;     // Server to connect to
    int server_port;       // Server port
    GtkListStore *servers; // Previous servers
    char *username;        // Login username
    char *password;        // Login password
    int hide_password;     // Hide password
    
    // Game creation options  
    char *game_desc;       // Game description
    char *game_pass;       // Game password
    int multi_min;         // Min multiplayer players
    int multi_max;         // Max multiplayer players
    
    // Save/Export options
    int auto_save;         // Enable autosave
    int export_cards;      // Export card locations
    int auto_export;       // Auto-export at game end
    char *last_save;       // Last save location
    char *data_folder;     // Data folder location
    char *export_folder;   // Export folder location
    
    // Logging options
    int verbose_log;       // Verbose logging
    int draw_log;          // Log card draws
    int discard_log;       // Log discards
} options;
```

## Visual Presentation

### Window System

#### Constants and Defaults
```c
#define TITLE "Race for the Galaxy " RELEASE  // Window title
#define SERVER_1 "rftg.plingri.net"          // Primary server
#define SERVER_2 "keldon.net"                // Backup server

// Default options
options opt = {
    3,  // num_players (default: 3)
};

// Game state flags
#define TAMPERED_SAVE  1 << 1  // Save game modified
#define TAMPERED_LOAD  1 << 2  // Load game modified
#define TAMPERED_SEED  1 << 3  // RNG seed modified
#define TAMPERED_UNDO  1 << 4  // Undo used
#define TAMPERED_LOOK  1 << 5  // Cards revealed
#define TAMPERED_DEBUG 1 << 6  // Debug mode used

#### Window Configuration
```c
struct window_info {
    int width;          // Window width (default: 1024)
    int height;         // Window height (default: 768)
    int fullscreen;     // Fullscreen flag
    int scale_factor;   // UI scaling (default: 1.0)
    char *title;        // Window title
    int tampered;       // Game state modification flags
    int replay_mode;    // Whether in replay mode
    int num_undo;       // Current undo position
    int max_undo;       // Total saved undo positions
    int *orig_log[MAX_PLAYER];  // Original choice logs
};
```

### Card Rendering
1. **Card Dimensions**
   - Width: 90 pixels
   - Height: 130 pixels
   - Border: 1 pixel black
   - Corner radius: 5 pixels

2. **Card Elements**
   - Name bar: 15 pixels high, top
   - Cost circle: Top right, 20x20 pixels
   - VP circle: Bottom right, 20x20 pixels
   - Military strength: Red shield icon
   - Good type: Colored circle on world cards
   - Powers: Bottom section icons

3. **Card States**
   - Normal: Full color
   - Selected: Yellow highlight
   - Disabled: Grayscale
   - Highlighted: White border
   - Face down: Card back texture

### Game Board Layout
1. **Player Areas**
   - Tableau: Grid layout, 4x3
   - Hand: Bottom of screen
   - VP/Military tracking: Right side
   - Action selection: Left side

2. **Shared Areas**
   - Draw deck: Top right
   - Discard pile: Below draw deck
   - Phase track: Top of screen
   - Victory point pool: Top right
   - Goal tiles: Top left (if enabled)

### Animation System
1. **Card Movements**
   - Draw: 0.3 second duration
   - Play: 0.4 second duration
   - Discard: 0.2 second duration
   - Curve: Quadratic easing

2. **Effect Visualization**
   - VP gain: Flying numbers
   - Military strength: Pulsing red glow
   - Power activation: Blue sparkle
   - Error: Red flash
   - Selection: Yellow pulse

### Interface Elements
1. **Buttons**
   - Size: 100x30 pixels
   - Font: Arial 12pt
   - Colors: 
     - Normal: #4A90E2
     - Hover: #357ABD
     - Pressed: #2A6496
     - Disabled: #CCCCCC

2. **Text Elements**
   - Game text: Arial 14pt
   - Card names: Arial Bold 12pt
   - VP/Points: Arial Bold 16pt
   - Error messages: Arial 12pt red

## Game Rules Implementation

### Random Number Generation
```c
// Original implementation from engine.c
int simple_rand(unsigned int *seed) {
    *seed = *seed * 1664525 + 1013904223;
    return ((unsigned)(*seed/65536) % 32768);
}
```
- Must use 32-bit unsigned integer arithmetic
- Multiplier: 1664525
- Increment: 1013904223
- Output transformation: (seed/65536) % 32768
- Random seed must be maintained exactly as in original

### Card System

#### Card Types
1. Worlds (type=1)
   - Regular worlds
   - Military worlds (requires military strength)
   - Windfall worlds (no initial good)
2. Developments (type=2)
   - Regular developments
   - 6-cost developments (special VP conditions)

#### Card Memory Layout
```c
typedef struct card {
    int type;           // World (1) or Development (2)
    int cost;           // Base cost 0-6
    int vp;             // Victory points
    int flags;          // Bit flags for special properties
    int good_type;      // Type of good (0 for none)
    int good_count;     // Number of goods
    power powers[];     // Array of powers
} card;
```

#### Card Flags
```c
// Card flags (must use exact 64-bit values)
#define FLAG_MILITARY        (1ULL << 0)   // Military world
#define FLAG_WINDFALL        (1ULL << 1)   // Windfall world
#define FLAG_START           (1ULL << 2)   // Starting world

#define FLAG_START_RED       (1ULL << 3)   // Red starting world
#define FLAG_START_BLUE      (1ULL << 4)   // Blue starting world

#define FLAG_PROMO           (1ULL << 5)   // Promotional card

#define FLAG_REBEL          (1ULL << 6)    // Rebel card
#define FLAG_UPLIFT         (1ULL << 7)    // Uplift power
#define FLAG_ALIEN          (1ULL << 8)    // Alien card
#define FLAG_TERRAFORMING   (1ULL << 9)    // Terraforming power
#define FLAG_IMPERIUM       (1ULL << 10)   // Imperium card
#define FLAG_CHROMO         (1ULL << 11)   // Chromosome world

#define FLAG_PRESTIGE       (1ULL << 12)   // Prestige card

#define FLAG_STARTHAND_3    (1ULL << 13)   // Start with 3 in hand
#define FLAG_START_SAVE     (1ULL << 14)   // Save at start
#define FLAG_DISCARD_TO_12  (1ULL << 15)   // Discard to 12
#define FLAG_GAME_END_14    (1ULL << 16)   // Game end at 14
#define FLAG_TAKE_DISCARDS  (1ULL << 17)   // Take discards
#define FLAG_SELECT_LAST    (1ULL << 18)   // Select last
#define FLAG_EXTRA_SURVEY   (1ULL << 19)   // Extra survey

#define FLAG_NO_PRODUCE     (1ULL << 20)   // Cannot produce
#define FLAG_DISCARD_PRODUCE (1ULL << 21)  // Discard to produce

#define FLAG_XENO           (1ULL << 22)   // Xeno card
#define FLAG_ANTI_XENO      (1ULL << 23)   // Anti-xeno card
#define FLAG_PEACEFUL       (1ULL << 24)   // Peaceful card

// Good types (must use exact values)
#define GOOD_ANY      1     // Any good
#define GOOD_NOVELTY  2     // Novelty good
#define GOOD_RARE     3     // Rare good
#define GOOD_GENE     4     // Gene good
#define GOOD_ALIEN    5     // Alien good
#define MAX_GOOD      6

// Card locations (must preserve exact values)
#define WHERE_DECK     0      // In draw deck
#define WHERE_DISCARD  1      // In discard pile
#define WHERE_HAND     2      // In player's hand
#define WHERE_ACTIVE   3      // In player's tableau
#define WHERE_GOOD     4      // Used as a good
#define WHERE_VP       5      // Used to pay VP
#define WHERE_SAVED    6      // Saved for later (special powers)
#define WHERE_PRESTIGE 7      // Used to pay prestige
#define MAX_WHERE      8      // Number of locations

### Game State

#### Player State
```c
typedef struct player {
    int hand[MAX_HAND];         // Cards in hand
    int table[MAX_ACTIVE];      // Active cards
    int vp;                     // Victory points
    int military;               // Military strength
    int prestige;              // Prestige points
    int goods[MAX_GOOD];       // Goods on cards
    int action;                // Selected action
    unsigned int seed;         // RNG seed
} player;
```

#### Game Phases
```c
// Round phases (exact values must be preserved)
#define PHASE_ACTION   0    // Action selection
#define PHASE_EXPLORE  1    // Explore phase
#define PHASE_DEVELOP  2    // Develop phase
#define PHASE_SETTLE   3    // Settle phase
#define PHASE_CONSUME  4    // Consume phase
#define PHASE_PRODUCE  5    // Produce phase
#define PHASE_DISCARD  6    // Discard phase
#define MAX_PHASE      7

// Action choices (exact values must be preserved)
#define ACT_GAME_START     -2    // Game start special action
#define ACT_ROUND_START    -1    // Round start special action
#define ACT_SEARCH         0     // Search action (expansions)
#define ACT_EXPLORE_5_0    1     // Explore: Draw 5, keep 0
#define ACT_EXPLORE_1_1    2     // Explore: Draw 1, keep 1
#define ACT_DEVELOP        3     // Develop action
#define ACT_DEVELOP2       4     // Advanced develop action
#define ACT_SETTLE         5     // Settle action
#define ACT_SETTLE2        6     // Advanced settle action
#define ACT_CONSUME_TRADE  7     // Consume-trade action
#define ACT_CONSUME_X2     8     // Consume-x2 action
#define ACT_PRODUCE        9     // Produce action
#define ACT_ROUND_END      10    // Round end special action
#define MAX_ACTION         10

#define ACT_MASK           0x7f  // Action mask
#define ACT_PRESTIGE       0x80  // Prestige action flag

// Session status types (must preserve exact values)
#define SS_EMPTY     0      // Empty session
#define SS_WAITING   1      // Waiting for players
#define SS_STARTED   2      // Game in progress
#define SS_DONE      3      // Game completed
#define SS_ABANDONED 4      // Game abandoned
```

Phase Implementation Details:
1. **Explore Phase**
   - Draw X+1, keep X variant
   - Draw 1, keep 1 + discard bonus variant
   - Powers resolve in exact tableau order
   
3. **Settle**
   - Place world card
   - Check military strength
   - Pay cards or use military
   
4. **Consume**
   - Trade goods (2x VPs)
   - Consume powers
   - Order: Left to right, top to bottom
   
5. **Produce**
   - Add goods to production worlds
   - Skip windfall worlds
   - Apply production powers

### Power System

#### Power Types
```c
// Search categories (must preserve exact values)
#define SEARCH_DEV_MILITARY      0     // Military development
#define SEARCH_MILITARY_WINDFALL 1     // Military windfall world
#define SEARCH_PEACEFUL_WINDFALL 2     // Peaceful windfall world
#define SEARCH_CHROMO_WORLD      3     // Chromosome world
#define SEARCH_ALIEN_WORLD       4     // Alien world
#define SEARCH_CONSUME_TWO       5     // Double consume power
#define SEARCH_MILITARY_5        6     // Military-5 world
#define SEARCH_6_DEV            7      // 6-cost development
#define SEARCH_TAKEOVER         8      // Takeover target
#define MAX_SEARCH              9

// Power flags per phase (must preserve exact values)
// Explore phase powers
#define P1_DRAW               (1ULL << 0)  // Draw bonus
#define P1_KEEP               (1ULL << 1)  // Keep bonus
#define P1_DISCARD_ANY        (1ULL << 2)  // Discard to draw
#define P1_DISCARD_PRESTIGE   (1ULL << 3)  // Discard for prestige
#define P1_ORB_MOVEMENT       (1ULL << 4)  // Orb movement
#define P1_PER_REBEL_MILITARY (1ULL << 5)  // Per rebel military

// Develop phase powers
#define P2_DRAW               (1ULL << 0)  // Draw bonus
#define P2_REDUCE             (1ULL << 1)  // Cost reduction
#define P2_DRAW_AFTER         (1ULL << 2)  // Draw after develop
#define P2_EXPLORE            (1ULL << 3)  // Explore bonus
#define P2_DISCARD_REDUCE     (1ULL << 4)  // Discard to reduce
#define P2_SAVE_COST          (1ULL << 5)  // Save payment
#define P2_PRESTIGE          (1ULL << 6)   // Prestige bonus
#define P2_PRESTIGE_REBEL    (1ULL << 7)   // Rebel prestige
#define P2_PRESTIGE_SIX      (1ULL << 8)   // Six-cost prestige
#define P2_CONSUME_RARE      (1ULL << 9)   // Consume rare

// Settle phase powers
#define P3_REDUCE             (1ULL << 0)  // Cost reduction
#define P3_NOVELTY            (1ULL << 1)  // Novelty discount
#define P3_RARE               (1ULL << 2)  // Rare discount
#define P3_GENE               (1ULL << 3)  // Gene discount
#define P3_ALIEN              (1ULL << 4)  // Alien discount
#define P3_DISCARD           (1ULL << 5)   // Discard power
#define P3_REDUCE_ZERO       (1ULL << 6)   // Zero cost
#define P3_MILITARY_HAND     (1ULL << 7)   // Military from hand

// Card power structure
typedef struct power {
    int phase;      // Phase when power is active
    int code;       // Power type code
    int value;      // Power value/strength
    int times;      // Number of uses (if applicable)
} power;
```

#### Additional Phase Powers
```c
// Settle phase additional powers
#define P3_EXTRA_MILITARY     (1ULL << 8)   // Extra military
#define P3_AGAINST_REBEL      (1ULL << 9)   // Against rebels
#define P3_AGAINST_CHROMO     (1ULL << 10)  // Against chromosomes
#define P3_PER_MILITARY       (1ULL << 11)  // Per military
#define P3_PER_CHROMO         (1ULL << 12)  // Per chromosome
#define P3_IF_IMPERIUM        (1ULL << 13)  // If imperium

#define P3_PAY_MILITARY       (1ULL << 14)  // Pay with military
#define P3_PAY_DISCOUNT       (1ULL << 15)  // Payment discount
#define P3_PAY_PRESTIGE       (1ULL << 16)  // Pay with prestige

#define P3_CONQUER_SETTLE     (1ULL << 17)  // Conquer and settle
#define P3_NO_TAKEOVER        (1ULL << 18)  // Prevent takeover

// Important power masks
#define P3_TAKEOVER_MASK (P3_TAKEOVER_REBEL | P3_TAKEOVER_IMPERIUM | \
                         P3_TAKEOVER_MILITARY | P3_PRESTIGE_TAKEOVER)

#define P3_CONDITIONAL_MILITARY (P3_NOVELTY | P3_RARE | P3_GENE | P3_ALIEN | \
       P3_DISCARD | P3_AGAINST_REBEL | P3_CONSUME_NOVELTY | P3_CONSUME_RARE | \
       P3_CONSUME_ALIEN | P3_CONSUME_PRESTIGE | P3_XENO)

// Consume phase powers
#define P4_TRADE_ANY          (1ULL << 0)   // Trade any good
#define P4_TRADE_NOVELTY      (1ULL << 1)   // Trade novelty
#define P4_TRADE_RARE         (1ULL << 2)   // Trade rare
#define P4_TRADE_GENE         (1ULL << 3)   // Trade gene
#define P4_TRADE_ALIEN        (1ULL << 4)   // Trade alien
#define P4_TRADE_THIS         (1ULL << 5)   // Trade specific
#define P4_TRADE_BONUS_CHROMO (1ULL << 6)   // Trade chromosome bonus

#define P4_NO_TRADE           (1ULL << 7)   // Prevent trade

#define P4_CONSUME_ANY        (1ULL << 10)  // Consume any good
#define P4_CONSUME_TWO        (1ULL << 16)  // Consume two goods
#define P4_CONSUME_3_DIFF     (1ULL << 17)  // Consume three different
#define P4_CONSUME_N_DIFF     (1ULL << 18)  // Consume N different
#define P4_CONSUME_ALL        (1ULL << 19)  // Consume all goods

// Produce phase powers
#define P5_PRODUCE            (1ULL << 0)   // Production world
#define P5_WINDFALL          (1ULL << 1)    // Windfall world
#define P5_NOT_THIS          (1ULL << 2)    // Skip this world
#define P5_DRAW_EACH         (1ULL << 3)    // Draw per production
#define P5_DISCARD_PRODUCE   (1ULL << 4)    // Discard to produce
#define P5_DRAW_IF_PRODUCED  (1ULL << 5)    // Draw if produced

#### Phase-Specific Powers
1. Explore
   - DRAW_FIRST: Draw cards first (P1_DRAW)
   - KEEP_FIRST: Keep cards first (P1_KEEP)
   - DISCARD_TO_DRAW: Discard for draws (P1_DISCARD_ANY)
   
2. Develop
   - REDUCE: Cost reduction (P2_REDUCE)
   - PAY_DISCOUNT: Payment discount (P2_SAVE_COST)
   - DRAW_AFTER: Draw after develop (P2_DRAW_AFTER)
   
3. Settle
   - MILITARY: Military strength
   - REDUCE_SETTLE: Settlement discount
   - PLACE_MILITARY: Military placement
   
4. Consume
   - CONSUME_ANY: Consume any good
   - TRADE_ACTION: Trade action bonus
   - VP_CONSUME: VP for consuming
   
5. Produce
   - PRODUCE: Production power
   - DRAW_PRODUCE: Draw on produce
   - WINDFALL_PRODUCE: Windfall production

### Victory Point Calculation

#### Base Victory Points
- Card VP values
- Goods on cards (consumption)
- 6-cost development bonuses
- Prestige points (if applicable)

#### Special Victory Point Types
```c
// Special VP types (must preserve exact values)
#define VP_NOVELTY_PRODUCTION   0     // Novelty production worlds
#define VP_RARE_PRODUCTION      1     // Rare production worlds
#define VP_GENE_PRODUCTION      2     // Gene production worlds
#define VP_ALIEN_PRODUCTION     3     // Alien production worlds

#define VP_NOVELTY_WINDFALL     4     // Novelty windfall worlds
#define VP_RARE_WINDFALL        5     // Rare windfall worlds
#define VP_GENE_WINDFALL        6     // Gene windfall worlds
#define VP_ALIEN_WINDFALL       7     // Alien windfall worlds

#define VP_DEVEL_EXPLORE        8     // Explore developments
#define VP_WORLD_EXPLORE        9     // Explore worlds
#define VP_DEVEL_TRADE         10     // Trade developments
#define VP_WORLD_TRADE         11     // Trade worlds
#define VP_DEVEL_CONSUME       12     // Consume developments
#define VP_WORLD_CONSUME       13     // Consume worlds

#define VP_SIX_DEVEL           14     // 6-cost developments
#define VP_DEVEL               15     // Any development
#define VP_WORLD               16     // Any world

#define VP_NONMILITARY_WORLD   17    // Non-military worlds
#define VP_NONMILITARY_TRADE   18    // Non-military trade worlds

#define VP_REBEL_FLAG          19     // Rebel cards
#define VP_ALIEN_FLAG          20     // Alien cards
#define VP_TERRAFORMING_FLAG   21     // Terraforming cards
#define VP_UPLIFT_FLAG         22     // Uplift cards
#define VP_IMPERIUM_FLAG       23     // Imperium cards
#define VP_CHROMO_FLAG         24     // Chromosome worlds

#define VP_MILITARY            25     // Military worlds
#define VP_TOTAL_MILITARY      26     // Total military strength
```

#### Special VP Conditions
1. 6-Cost Developments
   - Count specific card types using VP flags
   - Apply multipliers based on world counts
   - Process special conditions
   
2. Goal Tiles
   - First to achieve condition
   - Most of specific type
   - Special combinations

### Game Flow

#### Turn Structure
1. **Action Selection Phase**
   - Each player selects one action card
   - Actions revealed simultaneously
   - Bonus markers updated
   
2. **Phase Resolution**
   - Phases executed in fixed order
   - Active player resolves first
   - Tie-breakers based on first player

#### Action Resolution Details
1. **Explore Action**
   ```c
   struct explore_action {
       int type;              // 1=+5, 2=+1,+1
       int cards_drawn;       // Number to draw
       int cards_kept;        // Number to keep
       int bonus_drawn;       // Additional from powers
       int bonus_kept;        // Additional kept
   };
   ```
   - Draw cards first
   - Apply any "look first" powers
   - Select cards to keep
   - Discard remainder

2. **Develop Action**
   ```c
   struct develop_action {
       int card_played;       // Development card ID
       int base_cost;        // Original cost
       int final_cost;       // After reductions
       int[] payments;       // Cards used to pay
   };
   ```
   - Check cost and reductions
   - Pay cards from hand
   - Place development
   - Resolve powers

3. **Settle Action**
   ```c
   struct settle_action {
       int world_played;      // World card ID
       int military_used;     // Military strength
       int[] payments;        // Cards used to pay
       int takeover_target;   // -1 if none
   };
   ```
   - Check requirements
   - Apply military/payment
   - Place world
   - Add initial good if needed

4. **Consume Action**
   ```c
   struct consume_action {
       int trade_good;        // Good used for trade
       int trade_vp;         // VPs from trade
       struct {
           int good;         // Good consumed
           int power_used;   // Power card ID
           int vp_gained;    // VPs earned
       } consume_actions[];
   };
   ```
   - Trade action (if selected)
   - Process consume powers
   - Award victory points
   - Remove used goods

5. **Produce Action**
   ```c
   struct produce_action {
       int[] production_worlds;   // Worlds producing
       int[] windfall_worlds;    // Windfall produced
       int[] goods_added;        // Good placements
   };
   ```
   - Regular production first
   - Windfall production
   - Resolve draw powers

### Client State Management

#### Game Restart Reasons
```c
// Must preserve exact values for compatibility
#define RESTART_NEW        1     // Start new game
#define RESTART_NONE       2     // No restart needed
#define RESTART_LOAD       3     // Load saved game
#define RESTART_RESTORE    4     // Restore game
#define RESTART_UNDO       5     // Undo move
#define RESTART_UNDO_ROUND 6     // Undo whole round
#define RESTART_UNDO_GAME  7     // Undo to game start
#define RESTART_REDO       8     // Redo move
#define RESTART_REDO_ROUND 9     // Redo whole round
#define RESTART_REDO_GAME  10    // Redo to latest
#define RESTART_REPLAY     11    // Start replay
#define RESTART_CURRENT    12    // Current game state
```

#### Game List Column IDs
```c
// Must preserve exact column order
#define GAME_COL_ID                0   // Game ID
#define GAME_COL_DESC_NAME         1   // Game description
#define GAME_COL_DESC_NAME_CMP     2   // For sorting
#define GAME_COL_CREATOR_OFFLINE   3   // Creator status
#define GAME_COL_CREATOR_CMP       4   // For sorting
#define GAME_COL_PASSWORD          5   // Has password
#define GAME_COL_MIN_PLAYERS       6   // Min players
#define GAME_COL_MAX_PLAYERS       7   // Max players
#define GAME_COL_PLAYERS_STR       8   // Player list
#define GAME_COL_EXPANSION         9   // Expansion level
#define GAME_COL_EXPANSION_STR    10   // Expansion name
#define GAME_COL_ADVANCED         11   // Advanced game
#define GAME_COL_DISABLE_GOAL     12   // Goals disabled
#define GAME_COL_DISABLE_TO       13   // Takeover disabled
#define GAME_COL_NO_TIMEOUT       14   // No timeout
#define GAME_COL_SELF             15   // Own game
#define GAME_COL_CHECK_VISIBLE    16   // Visibility
#define GAME_COL_WEIGHT           17   // Sort weight
#define GAME_MAX_COLUMN           18
```

## Graphics System

### Card Rendering
```c
// Card image specifications
#define CARD_WIDTH 300      // Base card width
#define CARD_HEIGHT 420     // Base card height
#define CARD_SCALE 0.4      // Default display scale

// Image assets
typedef struct card_images {
    GdkPixbuf *full_size;   // Full resolution image
    GdkPixbuf *scaled;      // Scaled for display
    GdkPixbuf *mini;        // Mini version for hand
    int cached;            // Cache status
} card_images;

// Card visual elements
typedef struct card_graphics {
    int cost;              // Cost circle position
    int vp;               // VP badge position
    int military;         // Military strength
    rectangle text_area;   // Text placement
    rectangle art_area;    // Artwork placement
    point good_slots[4];   // Good placement positions
} card_graphics;

// Card highlighting
typedef struct highlight_info {
    int type;             // Highlight type
    int alpha;            // Transparency
    GdkColor color;       // Highlight color
    int pulsing;         // Animation flag
} highlight_info;
```

### Animation System
```c
// Animation types
#define ANIM_NONE      0    // No animation
#define ANIM_DEAL      1    // Deal card
#define ANIM_PLAY      2    // Play to tableau
#define ANIM_DISCARD   3    // Discard card
#define ANIM_SLIDE     4    // Slide card
#define ANIM_FLIP      5    // Flip card
#define ANIM_GOOD      6    // Place good

// Animation timing
#define ANIM_DURATION  250  // Base duration (ms)
#define ANIM_FPS       60   // Target framerate

// Animation queue
typedef struct anim_queue {
    animation *anims[MAX_ANIM];  // Active animations
    int count;                   // Queue size
    GTimer *timer;               // Animation timer
    int processing;              // Processing flag
} anim_queue;

// Animation callbacks
void (*anim_complete)(animation *a);
void (*anim_update)(animation *a, double progress);
```

### User Interface Layout
```c
// Window layout
typedef struct layout_info {
    int width;            // Window width
    int height;           // Window height
    double scale;         // UI scale factor
    
    // Areas
    rectangle hand;       // Hand area
    rectangle tableau;    // Tableau area
    rectangle actions;    // Action buttons
    rectangle vp;        // VP display
    rectangle log;       // Game log
    
    // Card spacing
    int card_spacing;    // Between cards
    int row_spacing;     // Between rows
    double overlap;      // Card overlap
} layout_info;

// UI Components
typedef struct ui_components {
    GtkWidget *action_buttons[8];  // Action selection
    GtkWidget *phase_labels[7];    // Phase indicators
    GtkWidget *vp_counter;         // VP display
    GtkWidget *card_preview;       // Card zoom
    GtkWidget *player_info[6];     // Player status
    GtkWidget *chat_entry;         // Chat input
} ui_components;
```

### Card Preview System
```c
// Preview modes
#define PREVIEW_NONE    0   // No preview
#define PREVIEW_HOVER   1   // Mouse hover
#define PREVIEW_LOCKED  2   // Locked view
#define PREVIEW_ZOOM    3   // Temporary zoom

// Preview window
typedef struct preview_window {
    GtkWidget *window;     // Preview window
    GdkPixbuf *image;     // Current image
    card *current;         // Displayed card
    int mode;             // Display mode
    point position;       // Window position
    int visible;         // Visibility flag
} preview_window;

// Preview functions
void show_preview(card *c, int mode);
void update_preview_position(int x, int y);
void hide_preview(void);
```

### Card Library System

#### Design Database
```c
// Global card design database
struct design {
    char *name;           // Card name
    char *short_name;     // Short name
    int type;            // Card type
    int cost;            // Base cost
    int vp;              // Victory points
    uint64_t flags;      // Card flags
    int good_type;       // Good type (0 for none)
    int good_count;      // Initial goods
    power powers[MAX_POWER];  // Card powers
    vp_bonus bonus[MAX_VP_BONUS]; // VP bonuses
    char *text;          // Card text
} library[AVAILABLE_DESIGN];

// Design tracking
int num_design;          // Number of loaded designs
```

#### Name Tables
```c
// Must preserve exact strings
static char *flag_name[] = {
    "MILITARY",
    "WINDFALL",
    "START",
    "START_RED", 
    "START_BLUE",
    "PROMO",
    "REBEL",
    "UPLIFT",
    "ALIEN",
    "TERRAFORMING",
    "IMPERIUM", 
    "CHROMO",
    "PRESTIGE",
    "STARTHAND_3",
    "START_SAVE",
    "DISCARD_TO_12",
    "GAME_END_14",
    "TAKE_DISCARDS",
    "SELECT_LAST",
    "EXTRA_SURVEY",
    "NO_PRODUCE",
    "DISCARD_PRODUCE",
    "XENO",
    "ANTI_XENO",
    NULL
};

static char *good_name[] = {
    "",
    "ANY", 
    "NOVELTY",
    "RARE", 
    "GENE",
    "ALIEN",
    NULL
};
```

### Detailed Game Rules

#### Card Interactions
1. **Power Resolution Order**
   - Left to right in tableau
   - Top to bottom on card
   - Mandatory before optional
   - Specific timing rules:
     ```c
     enum power_timing {
         IMMEDIATE,     // On card play
         PHASE_START,   // Start of phase
         PHASE_ACTION,  // During phase
         PHASE_END,     // End of phase
         GAME_END      // Final scoring
     };
     ```

2. **Military Strength**
   - Base strength from cards
   - Temporary bonuses
   - Specific world requirements
   - Rebel/Alien military worlds

3. **Good Management**
   ```c
   struct good_info {
       int type;           // Good type
       int world_index;    // World card index
       int count;          // Number of goods
       int is_windfall;    // Windfall flag
   };
   ```
   - Maximum 3 per world
   - Windfall restrictions
   - Good type matching
   - Consumption order

4. **Victory Point Calculation**
   ```c
   struct vp_source {
       int card_vp;        // Printed card VP
       int good_vp;        // VP from goods
       int bonus_vp;       // 6-cost bonuses
       int goal_vp;        // Goal tile VP
       int prestige_vp;    // Prestige VP
   };
   ```
   - Base card values
   - Consumed goods
   - Development bonuses
   - Goal achievements
   - Prestige points

## Artificial Intelligence System

### Neural Network Implementation

#### Network Constants
```c
// Network architecture constants (must match original exactly)
#define EVAL_HIDDEN 50      // Evaluator hidden nodes
#define ROLE_HIDDEN 50      // Role predictor hidden nodes
#define ROLE_OUT     7      // Role outputs (basic game)
#define ROLE_OUT_ADV 23     // Role outputs (advanced game)
#define ROLE_OUT_EXP3 15    // Role outputs (3rd expansion)
#define ROLE_OUT_ADV_EXP3 76 // Role outputs (advanced + 3rd exp)

// Leader tracking constants
#define LEADER_VP        0  // Victory points
#define LEADER_PRESTIGE  1  // Prestige points
#define LEADER_BUILT     2  // Built cards
#define LEADER_CARDS     3  // Cards in hand
#define LEADER_GOODS     4  // Goods on cards
#define MAX_LEADER       5  // Number of leader categories

#### Network Architecture
```c
typedef struct net {
    double alpha;           // Learning rate
    double error;           // Cumulative error
    double num_error;       // Number of error events (weighted)
    
    int num_inputs;         // Number of input nodes
    int num_hidden;         // Number of hidden nodes
    int num_output;         // Number of output nodes
    
    double **hidden_weight; // Hidden layer weights
    double **hidden_delta;  // Hidden weight deltas
    double **output_weight; // Output layer weights
    double **output_delta;  // Output weight deltas
    
    double *hidden_sum;     // Hidden node sums
    double *hidden_error;   // Hidden node error
    double *input_value;    // Current inputs
    double *prev_input;     // Previous inputs
    double *hidden_result;  // Hidden layer results
    double *net_result;     // Network outputs
    double *win_prob;       // Output probabilities
    
    double prob_sum;        // Probability normalization sum
    
    double **past_input;    // Training history inputs
    int *past_input_player; // Player who made moves
    int num_past;           // Number of past inputs
    int num_training;       // Training iterations completed
    
    char **input_name;      // Input feature names
} net;
```

#### Input Encoding (711 inputs)
1. **Card Counts (405 inputs)**
   - In hand: 0-1 normalized
   - In tableau: 0-1 normalized
   - VP chips: 0-1 normalized
   - Goods by type: 0-1 normalized
   
2. **Game State (156 inputs)**
   - Phase indicators
   - Action selection
   - Military strength
   - Current VP total
   - Prestige status
   
3. **Opponent Info (150 inputs)**
   - Tableau composition
   - VP estimation
   - Military strength
   - Action tendencies

#### Network Types
1. **Role Network**
   - Outputs: 7 (action probabilities)
   - Architecture: 711->100->7
   - Activation: tanh->softmax
   
2. **Value Network**
   - Outputs: 1 (win probability)
   - Architecture: 711->100->1
   - Activation: tanh->sigmoid

3. **Card Network**
   - Outputs: variable (legal moves)
   - Architecture: 711->100->moves
   - Activation: tanh->softmax

### AI Neural Network Implementation

#### Network Structure
```c
typedef struct net {
    // Learning parameters
    double alpha;          // Learning rate
    double error;          // Cumulative error
    double num_error;      // Number of error events (weighted by lambda)
    
    // Network architecture
    int num_inputs;        // Number of input nodes
    int num_hidden;        // Number of hidden nodes (50 for both networks)
    int num_output;        // Number of output nodes
    
    // Network weights and deltas
    double **hidden_weight;    // Hidden layer weights [inputs][hidden]
    double **hidden_delta;     // Hidden weight deltas
    double **output_weight;    // Output layer weights [hidden][outputs]
    double **output_delta;     // Output weight deltas
    
    // Node values
    double *hidden_sum;        // Hidden node sums
    double *hidden_error;      // Hidden node error
    double *input_value;       // Input values
    double *prev_input;        // Previous input values
    double *hidden_result;     // Hidden layer outputs
    double *net_result;        // Network outputs
    double *win_prob;          // Output probabilities
    double prob_sum;           // Probability normalization sum
    
    // Training history
    double **past_input;       // Past input sets
    int *past_input_player;    // Player who made input
    int num_past;              // Number of past inputs stored
    int num_training;          // Training iterations completed
    
    // Documentation
    char **input_name;         // Names of input features
} net;
```

#### Network Initialization

1. Evaluator Network
```c
// Create evaluator network
eval.alpha = 0.0001 * factor;  // Learning rate
// Size defined by:
#define EVAL_HIDDEN 50         // Hidden layer size

// Load from file:
// network/rftg.eval.<expansion>.<players><advanced>.net
```

2. Role Predictor Network
```c
// Create role predictor network
role.alpha = 0.0005 * factor;  // Learning rate
// Size defined by:
#define ROLE_HIDDEN 50         // Hidden layer size
// Output sizes:
#define ROLE_OUT      7        // Basic game
#define ROLE_OUT_ADV  23       // Advanced game
#define ROLE_OUT_EXP3 15       // Basic + Expansion 3
#define ROLE_OUT_ADV_EXP3 76   // Advanced + Expansion 3

// Load from file:
// network/rftg.role.<expansion>.<players><advanced>.net
```

### AI Training Process

#### Network File Format
The network implementation uses these key features:

1. Network Format & Storage
```c
// File Format (network/*.net):
// Line 1: [num_inputs] [num_hidden] [num_outputs]
// Lines 2+: Matrix weights, one per line:
//   - First [inputs+1]*[hidden] lines: hidden_weights[i][j]
//   - Next [hidden+1]*[outputs] lines: output_weights[i][j]
// Final lines: [feature_name] = name of input feature i
```

2. Weight Initialization
```c
static void init_weight(double *wgt) {
    *wgt = 0.2 * rand() / RAND_MAX - 0.1;  // Range: [-0.1, 0.1]
}
```

3. Forward Pass Implementation

a. Key Optimizations
- Sparse input handling: Only process changed inputs
- Special-case +1/-1 input changes for faster updates
- Numerical stability in softmax via adjustment term
- Bias nodes implemented as fixed 1.0 inputs
- Memory reuse for network state

b. Implementation
```c
void compute_net(net *learn) {
    // Hidden layer computation with optimizations
    for (i = 0; i < learn->num_inputs + 1; i++) {
        // Sparse update: only process changed inputs
        if (learn->input_value[i] != learn->prev_input[i]) {
            // Fast path for common +1/-1 changes
            if (learn->input_value[i] - learn->prev_input[i] == 1)
                for (j = 0; j < learn->num_hidden; j++)
                    learn->hidden_sum[j] += learn->hidden_weight[i][j];
            else if (learn->input_value[i] - learn->prev_input[i] == -1)
                for (j = 0; j < learn->num_hidden; j++)
                    learn->hidden_sum[j] -= learn->hidden_weight[i][j];
            else
                for (j = 0; j < learn->num_hidden; j++)
                    learn->hidden_sum[j] += learn->hidden_weight[i][j] * 
                        (learn->input_value[i] - learn->prev_input[i]);
            
            learn->prev_input[i] = learn->input_value[i];
        }
    }
    
    // Apply activation function
    for (i = 0; i < learn->num_hidden; i++)
        learn->hidden_result[i] = tanh(learn->hidden_sum[i]);
        
    // Output layer computation (with softmax)
    learn->prob_sum = 0.0;
    for (i = 0; i < learn->num_output; i++) {
        sum = 0.0;
        for (j = 0; j < learn->num_hidden + 1; j++)
            sum += learn->hidden_result[j] * learn->output_weight[j][i];
            
        if (!i) adj = -sum;  // Numerical stability
        learn->net_result[i] = exp(sum + adj);
        learn->prob_sum += learn->net_result[i];
    }
}
```

4. Training Implementation

a. Weight Updates (Backpropagation)
```c
void train_net(net *learn, double lambda, double *desired) {
    // Track training progress
    learn->num_error += lambda;
    
    // 1. Output Layer Updates
    for (i = 0; i < learn->num_output; i++) {
        // Compute error
        error = lambda * (learn->win_prob[i] - desired[i]);
        learn->error += error * error;
        
        // Compute output derivatives
        deriv = learn->win_prob[i] * (1.0 - learn->win_prob[i]);
        
        // Update output weights
        for (j = 0; j < learn->num_hidden; j++) {
            // Direct gradient
            corr = -error * learn->hidden_result[j] * deriv;
            
            // Cross-entropy derivative for softmax
            hderiv = deriv * learn->output_weight[j][i];
            for (k = 0; k < learn->num_output; k++) {
                if (i == k) continue;
                hderiv -= learn->output_weight[j][k] * 
                         learn->net_result[i] * learn->net_result[k] /
                         (learn->prob_sum * learn->prob_sum);
            }
            
            // Accumulate hidden errors
            learn->hidden_error[j] += error * hderiv;
            
            // Update output weights
            learn->output_delta[j][i] += learn->alpha * corr;
        }
        
        // Update output bias
        learn->output_delta[learn->num_hidden][i] += 
            learn->alpha * -error * deriv;
    }
    
    // 2. Hidden Layer Updates
    // Compute hidden node corrections
    double *hidden_corr = malloc(sizeof(double) * learn->num_hidden);
    for (i = 0; i < learn->num_hidden; i++) {
        // Hidden layer derivative
        deriv = 1 - (learn->hidden_result[i] * learn->hidden_result[i]);
        hidden_corr[i] = deriv * -learn->hidden_error[i] * learn->alpha;
    }
    
    // Update hidden weights
    for (i = 0; i < learn->num_inputs + 1; i++) {
        if (!learn->input_value[i]) continue;
        for (j = 0; j < learn->num_hidden; j++) {
            learn->hidden_delta[i][j] += hidden_corr[j] * 
                                       learn->input_value[i];
        }
    }
    free(hidden_corr);
}
```

b. Weight Application
```c
void apply_training(net *learn) {
    // Apply accumulated deltas to weights
    for (i = 0; i < learn->num_hidden + 1; i++)
        for (j = 0; j < learn->num_output; j++) {
            learn->output_weight[i][j] += learn->output_delta[i][j];
            learn->output_delta[i][j] = 0;
        }
        
    for (i = 0; i < learn->num_inputs + 1; i++)
        for (j = 0; j < learn->num_hidden; j++) {
            learn->hidden_weight[i][j] += learn->hidden_delta[i][j];
            learn->hidden_delta[i][j] = 0;
        }
}
```

5. Training State
```c
// Constants
#define PAST_MAX 120   // Max previous inputs stored

// Per-network training state
struct {
    double error;          // Cumulative error
    double num_error;      // Error events (weighted)
    int num_training;      // Training iterations
    double **past_input;   // Previous input sets [PAST_MAX][num_inputs]
    int *past_input_player;// Player who made inputs
    int num_past;          // Number of past inputs stored
} training_state;
```

#### Learning Parameters
```c
// Training configuration
struct train_config {
    double learning_rate;  // Default: 1.0
    int num_games;        // Default: 100
    int num_players;      // Default: 3
    int expansion;        // Default: 0
    int advanced;         // Default: 0
    int promo;           // Default: 0
};

// Training statistics
struct train_stats {
    int num_errors;      // Number of prediction errors
    double total_error;  // Cumulative error
    double factor;       // Learning rate factor
    int num_training;    // Training iterations
};
```

#### Network Initialization
```c
void make_learner(net *n, int inputs, int hidden, int outputs) {
    // Allocate arrays
    n->num_inputs = inputs;
    n->num_hidden = hidden;
    n->num_output = outputs;
    
    // Initialize weights randomly in [-0.5, 0.5]
    n->hidden_weight = malloc_2d_double(inputs, hidden);
    n->output_weight = malloc_2d_double(hidden, outputs);
    init_random_weights(n);
    
    // Zero deltas/errors
    n->hidden_delta = calloc_2d_double(inputs, hidden); 
    n->output_delta = calloc_2d_double(hidden, outputs);
}
```

#### Training Process

1. Configuration
   - Training parameters set via command-line:
     - `-n`: Number of training games (default 100)
     - `-p`: Number of players (default 3)  
     - `-f`: Learning rate factor
     - `-e`: Expansion level (0-6)
     - `-a`: Advanced game flag
     - `-o`: Promo cards flag
     - `-v`: Verbose output

2. Per Game Loop
   ```c
   // For each training game:
   - Initialize game state
   - Set session_id = -2 (learning mode)
   - Play rounds until game ends
   - Score game and declare winner
   - Call AI game_over() for each player
     - Update network weights based on game outcome
   - Clear choice logs
   ```

3. Choice Recording
   - Each player maintains a choice log
   - Records decisions made during gameplay
   - Used for backpropagation after game completion

4. Learning Process  
   - Forward pass during gameplay:
     - Network evaluates possible moves
     - Chooses move based on evaluation
   - Backward pass after game:
     - Updates weights based on game outcome
     - Uses recorded choices for error attribution

### AI Decision Making

The AI uses two neural networks:

1. Evaluator Network (`eval`)
   - Purpose: Evaluates game states and possible moves
   - Architecture:
     - Hidden layer size: 50 nodes
     - Learning rate: 0.0001 * factor
   - Stored in: `network/rftg.eval.<expansion>.<players><advanced>.net`

2. Role Predictor Network (`role`)
   - Purpose: Predicts opponent role choices
   - Architecture:
     - Hidden layer size: 50 nodes
     - Learning rate: 0.0005 * factor
   - Output sizes:
     - Basic game: 7 outputs
     - Advanced game: 23 outputs
     - Basic with expansion 3: 15 outputs
     - Advanced with expansion 3: 76 outputs
   - Stored in: `network/rftg.role.<expansion>.<players><advanced>.net`

#### Move Selection Process

1. Action Space
```c
// Basic game actions
enum {
    ACT_EXPLORE_5_0,      // Draw 5, keep 0
    ACT_EXPLORE_1_1,      // Draw 1, keep 1
    ACT_DEVELOP,          // Play development
    ACT_SETTLE,           // Play world
    ACT_CONSUME_TRADE,    // Trade good
    ACT_CONSUME_X2,       // Consume with 2x VPs
    ACT_PRODUCE           // Produce goods
};

// Advanced game action combinations
static int adv_combo[ROLE_OUT_ADV_EXP3][2] = {
    { ACT_EXPLORE_5_0, ACT_EXPLORE_1_1 },
    { ACT_EXPLORE_5_0, ACT_DEVELOP },
    { ACT_EXPLORE_5_0, ACT_SETTLE },
    // ... (76 total combinations)
};
```

2. State Features
```c
// Leader tracking metrics
#define LEADER_VP        0  // Victory points
#define LEADER_PRESTIGE  1  // Prestige points
#define LEADER_BUILT     2  // Cards built
#define LEADER_CARDS     3  // Cards in hand
#define LEADER_GOODS     4  // Goods on tableau
#define MAX_LEADER       5

// Game completion states
#define COMPLETE_ROUND   0  // Complete current round
#define COMPLETE_CHECK   1  // Check completion
#define COMPLETE_DEVSET  2  // Complete development/settlement
```

2. Game Simulation
   - Creates temporary copy of game state
   - Simulates possible moves to evaluate outcomes
   - Uses both networks to:
     - Evaluate resulting positions
     - Predict opponent responses

3. Simulation Process
```c
// Game state simulation
static void complete_turn(game *g, int partial) {
    // 1. Finish current phase for all players
    for (i = g->turn + 1; i < g->num_players; i++) {
        // Handle trade/consume actions
        if (g->cur_action == ACT_CONSUME_TRADE) {
            if (player_chose(g, i, ACT_CONSUME_TRADE))
                trade_action(g, i, 0, 1);
            while (consume_action(g, i));  // Use all consume powers
        }
        
        // Handle produce actions
        if (g->cur_action == ACT_PRODUCE)
            while (produce_action(g, i));
    }
    
    // 2. Resolve pending effects
    if (g->cur_action == ACT_SETTLE || g->cur_action == ACT_SETTLE2)
        resolve_takeovers(g);
    if (g->cur_action == ACT_PRODUCE) 
        phase_produce_end(g);
        
    // 3. Update game state
    clear_temp(g);          // Clear temporary flags
    check_goals(g);         // Check goal completion
    check_prestige(g);      // Update prestige points
    
    // 4. Complete remaining phases if needed
    for (i = g->cur_action + 1; i <= ACT_PRODUCE; i++) {
        if (partial == COMPLETE_DEVSET && i >= ACT_CONSUME_TRADE)
            break;
        if (partial == COMPLETE_CHECK) 
            break;
            
        g->cur_action = i;
        if (!g->action_selected[i]) 
            continue;
            
        // Execute phase actions
        switch(i) {
            case ACT_EXPLORE_5_0: phase_explore(g); break;
            case ACT_DEVELOP:     phase_develop(g); break;
            case ACT_SETTLE:      phase_settle(g); break;
            case ACT_CONSUME_TRADE: phase_consume(g); break;
            case ACT_PRODUCE:     phase_produce(g); break;
        }
    }
}
```

4. Decision Making Pipeline
   a. State Evaluation
      - Feed current state into evaluator network
      - Get base position score
      
   b. Move Generation
      - Generate all legal moves for current phase
      - For each move:
        1. Create game state copy
        2. Apply move in copy
        3. Simulate resulting position
        4. Evaluate new state with network
        
   c. Role Prediction
      - Use role network to predict opponent choices
      - Adjust move scores based on predictions
      - Weight: role_avg (running average of prediction accuracy)
      
   d. Move Selection
      - Choose move with highest adjusted score
      - Record in choice log:
        ```c
        struct {
            int *choice_log;     // Array of move choices
            int choice_size;     // Number of choices recorded
            int choice_pos;      // Current position in log
        } player;
        ```
1. **Action Selection**
   ```python
   def select_action(game_state):
       # Convert game state to network input
       inputs = encode_game_state(game_state)
       
       # Get action probabilities
       probs = role_network.forward(inputs)
       
       # Apply temperature
       probs = apply_temperature(probs, temp=1.0)
       
       # Select action
       return weighted_choice(probs)
   ```

2. **Card Selection**
   ```python
   def select_card(game_state, legal_cards):
       # Get card probabilities
       probs = card_network.forward(inputs)
       
       # Mask illegal moves
       probs = mask_illegal_moves(probs, legal_cards)
       
       # Select card
       return weighted_choice(probs)
   ```

#### Training System

1. **Self-Play Generation**
   ```python
   def generate_training_data():
       games_per_iteration = 10000
       moves_per_game = []
       
       for _ in range(games_per_iteration):
           game = Game()
           while not game.is_over():
               move = select_move(game)
               store_position(game, move)
               game.make_move(move)
           
           store_outcome(game)
   ```

2. **Network Updates**
   ```python
   def update_networks():
       # Sample batch
       batch_size = 1024
       positions = sample_positions(batch_size)
       
       # Update role network
       role_loss = train_role_network(positions)
       
       # Update value network
       value_loss = train_value_network(positions)
       
       # Update card network
       card_loss = train_card_network(positions)
   ```

3. **Training Parameters**
   ```python
   TRAINING_CONFIG = {
       'iterations': 100,
       'games_per_iter': 10000,
       'batch_size': 1024,
       'learning_rate': 0.001,
       'momentum': 0.9,
       'l2_reg': 0.0001,
       'temperature': 1.0
   }
   ```

### AI Behavior Calibration

#### Difficulty Levels
1. **Easy**
   - Temperature = 2.0
   - Random move probability = 0.1
   - Restricted search depth
   
2. **Medium**
   - Temperature = 1.0
   - Random move probability = 0.0
   - Full network evaluation
   
3. **Hard**
   - Temperature = 0.5
   - Value network guidance
   - Multiple rollouts
```

#### State Representation
- Card counts by type
- Military strength
- VP totals
- Goods by type
- Action selection probabilities

#### Training Process
1. Initial weights from file
2. Self-play iterations
3. Weight updates
4. Performance validation

### File Formats

#### Save Game Format
```c
struct save_game {
    char version[1024];  // Version string
    unsigned int start_seed; // Initial RNG seed
    int num_players;    // Number of players
    int expanded;       // Expansion level
    int advanced;       // Advanced game flag
    int goal_disabled;  // Goals disabled flag
    int takeover_disabled; // Takeovers disabled
    char campaign[1024]; // Campaign name or "none"
    struct {
        int choice_size;   // Size of choice log
        int choice_log[];  // Array of choices made
    } players[];       // Per-player state
    int deck[];        // Remaining deck
    int discard[];     // Discard pile
};

// Choice log data must be stored exactly as original
// Original choice log format preserved for compatibility
struct choice_data {
    int type;          // Choice type
    int arg1;          // First argument
    int arg2;          // Second argument
    int arg3;          // Third argument
};
```

#### Card File Format
```plaintext
N:card name
T:type:cost:vp
E@e0:n0@e1:n1[...]
G:goodtype
F:flags
P:phase:code:value:times
V:value:type:name
```

## Expansion Features

### Expansion Information
```c
expansion exp_info[] = {
    {
        "Base game only", "Base", 0,
        .max_players = 4,
    },
    {
        "The Gathering Storm", "TGS", 1,
        .max_players = 5,
        .has_goals = 1,
    },
    {
        "Rebel vs Imperium", "RvI", 6,
        .max_players = 6,
        .has_goals = 1,
        .has_takeovers = 1,
        .has_start_world_choice = 1,
    },
    {
        "The Brink of War", "BoW", 2,
        .max_players = 6,
        .has_goals = 1,
        .has_takeovers = 1,
        .has_prestige = 1,
        .has_start_world_choice = 1,
    },
    {
        "Alien Artifacts", "AA", 3,
        .max_players = 5,
        .has_start_world_choice = 1,
    },
    {
        "Xeno Invasion", "XI", 4,
        .max_players = 5,
        .has_start_world_choice = 1,
    },
    {
        "Rebel vs Imperium only", "RvIo", 5,
        .max_players = 5,
        .has_takeovers = 1,
    },
};

### Feature Availability
```c
struct exp_info {
    int has_goals;          // Goals available
    int has_takeover;       // Takeovers allowed
    int has_prestige;       // Prestige mechanics
    int has_scenarios;      // Campaign scenarios
    int search_allowed;     // Search action available
};
```

## Compatibility Requirements

### Random Seeds
- Must use same seed progression
- Must match original RNG output exactly
- Must handle seed overflow identically

### Card Order
- Must maintain exact shuffle algorithm
- Must preserve draw/discard order
- Must handle deck recycling identically

### Power Resolution
- Must resolve in identical order
- Must handle multiple powers correctly
- Must preserve all edge cases

### Save Compatibility
- Must read original save files
- Must produce identical saves
- Must handle all versions

### Cross-Platform
- Must maintain identical behavior
- Must handle endianness correctly
- Must preserve numeric precision

## Network Protocol

### Client-Server Communication

#### Network Constants
```c
// Buffer sizes
#define BUF_LEN 1024      // Message buffer length
#define HEADER_LEN 8      // Message header length

// Message Types (must use exact values)
#define MSG_LOGIN             1    // Login request
#define MSG_HELLO             2    // Server greeting
#define MSG_DENIED            3    // Access denied
#define MSG_GOODBYE           4    // Disconnect notification
#define MSG_PING             5     // Keep-alive ping

// Player management
#define MSG_PLAYER_NEW       10    // New player joined
#define MSG_PLAYER_LEFT      11    // Player disconnected

// Game management
#define MSG_OPENGAME         20    // Create new game
#define MSG_GAME_PLAYER      21    // Player in game info
#define MSG_CLOSE_GAME       22    // Close game
#define MSG_JOIN             23    // Join request
#define MSG_LEAVE            24    // Leave game
#define MSG_JOINACK          25    // Join accepted
#define MSG_JOINNAK          26    // Join rejected
#define MSG_CREATE           27    // Create game
#define MSG_START            28    // Start game
#define MSG_REMOVE           29    // Remove player
#define MSG_RESIGN           30    // Player resignation
#define MSG_ADD_AI           31    // Add AI player

// Game state
#define MSG_STATUS_META      40    // Game metadata
#define MSG_STATUS_PLAYER    41    // Player status
#define MSG_STATUS_CARD      42    // Card status
#define MSG_STATUS_GOAL      43    // Goal status
#define MSG_STATUS_MISC      44    // Misc status
#define MSG_LOG              45    // Game log
#define MSG_CHAT             46    // Chat message
#define MSG_WAITING          47    // Waiting notification
#define MSG_SEAT             48    // Seat assignment
#define MSG_GAMECHAT         49    // In-game chat
#define MSG_LOG_FORMAT       50    // Log formatting

// Game actions
#define MSG_CHOOSE           60    // Action choice
#define MSG_PREPARE          61    // Prepare for choice

// Game end
#define MSG_GAMEOVER         70    // Game over

// Connection states
#define CS_EMPTY             0     // No connection
#define CS_INIT              1     // Initializing
#define CS_LOBBY             2     // In lobby
#define CS_PLAYING           3     // In game
```

### Client Connection
```c
struct conn {
    int fd;                // Socket file descriptor
    int ai;                // AI client flag
    char buf[BUF_LEN];     // Input buffer
    int buf_full;          // Buffer used bytes
    char *out_buf;         // Output buffer
    int out_len;           // Output buffer used
    int out_size;          // Output buffer size
    int state;             // Connection state
    char user[80];         // Username
    char version[80];      // Client version
    int uid;               // User ID
    char addr[80];         // IP address
    int sid;               // Session ID
    int keepalive;         // Keepalive state
};
```

### Message Formats
1. **Connection**
   ```json
   {
       "type": "connect",
       "version": "0.9.5",
       "player_name": "string",
       "game_options": {
           "expansions": [0,1,2],
           "ai_players": 2,
           "advanced": true
       }
   }
   ```

2. **Game State**
   ```json
   {
       "type": "game_state",
       "current_phase": 0,
       "active_player": 1,
       "players": [{
           "vp": 12,
           "military": 3,
           "tableau": [1,4,7],
           "hand_size": 4
       }],
       "cards_remaining": 23
   }
   ```

3. **Action Selection**
   ```json
   {
       "type": "action",
       "player": 1,
       "action": 2,
       "targets": [3,4],
       "timestamp": 123456789
   }
   ```

### Error Handling
1. **Validation**
   - Version compatibility
   - Message sequence
   - Action legality
   - State consistency

2. **Recovery**
   - State synchronization
   - Client reconnection
   - Game restoration

## Campaign System

### Scenario Structure
```python
class Scenario:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.description = ""
        self.victory_condition = None
        self.starting_cards = []
        self.ai_behavior = {}
        self.special_rules = {}
```

### Campaign Progress
1. **Player Progress**
   - Completed scenarios
   - Unlocked content
   - Achievement tracking
   - Statistics recording

2. **AI Modifications**
   - Scenario-specific behaviors
   - Special card preferences
   - Strategic objectives
   - Difficulty scaling

## Performance Requirements

### Response Times
1. **UI Actions**
   - Card selection: <50ms
   - Action selection: <100ms
   - Animation: 60fps
   - State update: <16ms

2. **Network**
   - Message latency: <200ms
   - State sync: <500ms
   - Reconnection: <2s

3. **AI**
   - Move selection: <1s
   - Game analysis: <2s
   - Training iteration: <30m

## Core Game Engine Architecture

### State Machine Implementation
```c
// Game phase enumeration
typedef enum {
    PHASE_SELECT = 0,      // Action selection
    PHASE_EXPLORE = 1,     // Explore phase
    PHASE_DEVELOP = 2,     // Develop phase
    PHASE_SETTLE = 3,      // Settle phase
    PHASE_CONSUME = 4,     // Consume phase
    PHASE_PRODUCE = 5,     // Produce phase
    PHASE_END = 6         // End of round
} game_phase;

// Phase execution functions
void execute_explore(game *g);
void execute_develop(game *g);
void execute_settle(game *g);
void execute_consume(game *g);
void execute_produce(game *g);
```

### Card Resolution System
```c
// Card power types
typedef enum {
    P_DISCARD,            // Discard to use
    P_CONSUME_HAND,       // Consume from hand
    P_CONSUME_GOOD,       // Consume good
    P_CONSUME_PRESTIGE,   // Consume prestige
    P_TEMPORARY,          // Temporary power
    P_GAME_START,         // Start of game
    P_PREPARE,            // Phase preparation
    P_START,              // Phase start
    P_PLACE,              // Card placement
    P_CONSUME_3_DIFF,     // Consume three different
    P_CONSUME_N_DIFF,     // Consume N different
    P_CONSUME_ALL,        // Consume all goods
    P_PRODUCE,            // Production
    P_PRODUCE_PRESTIGE,   // Produce prestige
    P_VP,                // Victory points
    P_TAKEOVER,          // Military takeover
    P_END                // End of game
} power_type;

// Power resolution order
void resolve_powers(game *g, int type);
void check_triggers(game *g, card *c);
int compute_power_value(game *g, card *c, int type);
```

### Campaign Integration
```c
// Campaign structure
typedef struct campaign {
    char *name;           // Campaign name
    int num_scenarios;    // Number of scenarios
    scenario *scenarios;  // Scenario array
    int current;         // Current scenario
    int completed;       // Completion status
    void *custom_data;   // Custom scenario data
} campaign;

// Scenario management
void load_campaign(game *g, char *name);
void start_scenario(game *g, int index);
int check_victory_condition(game *g);
void apply_scenario_effects(game *g);
```

## Client Implementation 

### GTK Widget Hierarchy
```c
// Main window components
GtkWidget *main_window;      // Top level window
GtkWidget *game_area;        // Game display area
GtkWidget *hand_area;        // Hand cards area
GtkWidget *table_area;       // Played cards area
GtkWidget *action_area;      // Action selection
GtkWidget *log_view;         // Game log
GtkWidget *status_bar;       // Status display

// Card display widgets
typedef struct card_view {
    GtkWidget *widget;       // Card widget
    GdkPixmap *pixmap;      // Card image
    card *card_ptr;         // Game card pointer
    int x, y;              // Display position
    int width, height;     // Display size
    int highlighted;       // Highlight state
} card_view;
```

### Rendering Pipeline
```c
// Image management
void load_card_images(void);
void create_card_pixmap(card_view *view);
void draw_card(card_view *view, GdkDrawable *target);
void update_card_display(game *g);

// Animation system
typedef struct animation {
    card_view *card;        // Animated card
    int start_x, start_y;   // Start position
    int end_x, end_y;       // End position
    double progress;        // Animation progress
    GTimer *timer;         // Animation timer
} animation;

void start_animation(animation *a);
void update_animations(void);
```

### Resource Management
```c
// Image cache
typedef struct image_cache {
    GHashTable *images;     // Image lookup table
    int total_size;        // Cache size
    int max_size;         // Size limit
} image_cache;

// Memory management
void init_cache(void);
void clear_cache(void);
void cache_card_image(int id);
GdkPixbuf *get_card_image(int id);
```

## Save/Load System

### State Serialization
```c
// Save format version
#define SAVE_VERSION 0x0905

// Save file header
typedef struct save_header {
    uint32_t magic;         // Magic number
    uint32_t version;       // Format version
    uint32_t checksum;      // Data checksum
    uint32_t data_size;     // Content size
} save_header;

// Serialization functions
void save_game_state(game *g, FILE *fp);
game *load_game_state(FILE *fp);
void write_card_state(card *c, FILE *fp);
void read_card_state(card *c, FILE *fp);
```

### Resource Files
```c
// File paths
#define CONFIG_FILE    "rftg.cfg"
#define SAVE_DIR      "saves"
#define CAMPAIGN_DIR  "campaigns"
#define LOG_DIR       "logs"

// Resource management
void init_paths(void);
char *get_resource_path(char *name);
void ensure_directories(void);
void cleanup_temp_files(void);
```

### Resource Usage
1. **Memory**
   - Base game: <200MB
   - Full expansions: <500MB
   - AI models: <100MB
   - Card cache: <50MB

2. **Storage**
   - Installation: <1GB
   - Save games: <1MB each
   - Replay files: <100KB each
   - Training data: <5GB

3. **CPU**
   - Game logic: Single core
   - AI: Multi-threaded
   - Graphics: GPU preferred

## Testing Requirements

### Verification Tests
1. RNG Sequence Tests
   - Known seed progressions
   - Output distribution checks
   
2. Game State Tests
   - Card movement tracking
   - Power resolution order
   - VP calculation accuracy

## Network Protocol Specification

### Message Format
```c
// Message header
typedef struct msg_header {
    uint32_t type;          // Message type
    uint32_t length;        // Payload length
    uint32_t sequence;      // Sequence number
    uint32_t checksum;      // Message checksum
} msg_header;

// Message types
#define MSG_HELLO      0x01  // Initial connection
#define MSG_AUTH       0x02  // Authentication
#define MSG_CREATE     0x03  // Create game
#define MSG_JOIN       0x04  // Join game
#define MSG_STATE      0x05  // Game state
#define MSG_ACTION     0x06  // Player action
#define MSG_CHAT       0x07  // Chat message
#define MSG_ERROR      0x08  // Error condition
```

### State Synchronization
```c
// State update flags
#define UF_HAND       0x01  // Hand changed
#define UF_TABLE      0x02  // Table changed
#define UF_SCORE      0x04  // Score changed
#define UF_PHASE      0x08  // Phase changed
#define UF_ACTION     0x10  // Action changed
#define UF_ALL        0x1F  // All changed

// Sync functions
void send_state_update(game *g, int flags);
void handle_state_update(msg_header *msg);
void request_resync(void);
```

### Error Handling
```c
// Error codes
#define ERR_NONE      0x00  // No error
#define ERR_VERSION   0x01  // Version mismatch
#define ERR_AUTH      0x02  // Auth failed
#define ERR_FULL      0x03  // Game full
#define ERR_STATE     0x04  // State error
#define ERR_TIMEOUT   0x05  // Connection timeout
#define ERR_PROTOCOL  0x06  // Protocol error

// Recovery procedures
void handle_error(int code);
void attempt_reconnect(void);
void restore_game_state(void);
```

### Security
```c
// Authentication
#define AUTH_NONE     0x00  // No auth
#define AUTH_PASS     0x01  // Password
#define AUTH_TOKEN    0x02  // Auth token

// Encryption
#define ENCRYPT_NONE  0x00  // No encryption
#define ENCRYPT_SSL   0x01  // SSL/TLS
#define ENCRYPT_AES   0x02  // AES-256

// Security functions
void init_security(void);
void encrypt_message(msg_header *msg);
void decrypt_message(msg_header *msg);
void validate_message(msg_header *msg);
```

### Multiplayer Coordination

#### Game Creation
```c
// Game options
typedef struct game_options {
    int num_players;        // Required players
    int expansions;         // Enabled expansions
    int advanced;          // Advanced game
    int campaign;          // Campaign mode
    char password[32];     // Game password
    int ranked;            // Ranked game
    int time_limit;        // Turn time limit
} game_options;

// Game creation
int create_game(game_options *opt);
int join_game(int game_id, char *password);
void leave_game(void);
```

#### Player Management
```c
// Player status
#define PS_DISCONNECTED  0x00
#define PS_CONNECTED     0x01
#define PS_READY         0x02
#define PS_ACTIVE        0x03
#define PS_INACTIVE      0x04

// Player functions
void update_player_status(int player, int status);
void handle_disconnect(int player);
void transfer_host(int new_host);
```

#### Turn Management
```c
// Turn control
void start_turn(game *g);
void end_turn(game *g);
void process_timeout(game *g);
void sync_turn_timer(void);

// Action validation
int validate_action(game *g, int player, int action);
void broadcast_action(game *g, int player, int action);
void rollback_action(game *g, int action);
```

## Input Handling System

### Mouse Input
```c
// Mouse states
#define MOUSE_NONE     0   // No action
#define MOUSE_DOWN     1   // Button pressed
#define MOUSE_DRAG     2   // Dragging
#define MOUSE_UP       3   // Button released

// Input areas
typedef struct input_area {
    rectangle bounds;     // Clickable area
    int type;            // Area type
    void *data;          // Associated data
    int (*handler)(int event, int x, int y, void *data);
} input_area;

// Drag and drop
typedef struct drag_info {
    card_view *card;     // Dragged card
    point start;         // Start position
    point current;       // Current position
    int valid_target;    // Drop allowed
} drag_info;
```

### Keyboard Input
```c
// Key bindings
typedef struct key_binding {
    guint keyval;        // Key code
    GdkModifierType mods; // Modifiers
    void (*handler)(void); // Handler function
    char *description;    // Help text
} key_binding;

// Default bindings
#define KEY_EXPLORE1   GDK_KEY_1
#define KEY_EXPLORE2   GDK_KEY_2
#define KEY_DEVELOP    GDK_KEY_3
#define KEY_SETTLE     GDK_KEY_4
#define KEY_CONSUME    GDK_KEY_5
#define KEY_PRODUCE    GDK_KEY_6
#define KEY_CONFIRM    GDK_KEY_Return
#define KEY_CANCEL     GDK_KEY_Escape
```

### Input Management
```c
// Input modes
#define MODE_NORMAL    0   // Normal gameplay
#define MODE_CHOOSE    1   // Making choice
#define MODE_PREVIEW   2   // Card preview
#define MODE_DIALOG    3   // Dialog open

// Input context
typedef struct input_context {
    int mode;            // Current mode
    GSList *areas;       // Active areas
    drag_info drag;      // Drag state
    card_view *hover;    // Hovered card
    int blocked;         // Input blocked
    double last_click;   // Double-click
} input_context;

// Input functions
void handle_mouse_event(int type, int x, int y);
void handle_key_event(guint keyval, GdkModifierType mods);
void update_input_areas(void);
void clear_input_state(void);
```
```
   - Power resolution order
   - VP calculation accuracy
   
3. AI Behavior Tests
   - Decision matching
   - Learning convergence
   - Win rate statistics

### Compatibility Tests
1. Save/Load Tests
   - Original save files
   - Cross-version loading
   - State preservation
   
2. Replay Tests
   - Original game logs
   - Action sequence verification
   - Random seed tracking
   
3. Cross-Platform Tests
   - Bit-exact behavior
   - Numeric consistency
   - File format handling
