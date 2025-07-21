# Race for the Galaxy - Python Implementation

A faithful Python implementation of the Race for the Galaxy card game, designed to be fully compatible with the original C implementation.

## Project Status

This project is currently under development. The implementation follows the exact specifications defined in `../specifications.md` to ensure 100% compatibility with the original game.

## Project Structure

```
python_rftg/
├── src/
│   ├── core/        # Core game engine
│   ├── ui/          # Graphics and UI
│   ├── ai/          # AI system
│   ├── net/         # Network code
│   └── utils/       # Utilities
├── tests/           # Test suite
├── docs/            # Documentation
├── resources/       # Game assets
└── tools/           # Development tools
```

## Requirements

- Python 3.10 or higher
- PyQt6 for GUI
- NumPy for numerical operations
- PyTorch for AI implementation

## Installation

### Development Setup

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1

# Activate on Windows Command Prompt
venv\Scripts\activate.bat

# Activate on Linux/Mac
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Install in development mode:
```bash
pip install -e .
```

Note: The virtual environment is already configured in this project. Make sure to activate it before running any Python commands.

### Production Installation

```bash
pip install rftg-python
```

## Development Guidelines

### Specification Compliance

All implementations MUST conform exactly to the technical specifications defined in `../specifications.md`. The specifications document serves as the absolute source of truth for:

1. Data structures and type definitions
2. Function signatures and behavior  
3. Constants and enumeration values
4. Protocol definitions and formats
5. UI layouts and dimensions
6. Performance requirements
7. Compatibility requirements

### Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

### Code Quality

Format code:
```bash
black src/ tests/
```

Type checking:
```bash
mypy src/
```

Linting:
```bash
flake8 src/ tests/
```

## Compatibility

This implementation maintains compatibility with:
- Original C version 0.9.5
- Save file formats
- Network protocol versions
- AI model versions
- Replay files

## Features

### Completed
- Project structure setup
- Build system configuration
- Development environment

### In Progress
- Core game engine
- Card system implementation
- Game state management

### Planned
- Complete UI implementation
- AI system with neural networks
- Network multiplayer
- Campaign system
- Full test coverage

## Contributing

Please ensure all contributions:
1. Follow the exact specifications in `../specifications.md`
2. Include comprehensive tests
3. Maintain type hints throughout
4. Pass all code quality checks
5. Document any implementation decisions

## License

This project is licensed under the GNU General Public License v2 (GPLv2), maintaining compatibility with the original Race for the Galaxy implementation.

## Original Game

Race for the Galaxy is a card game designed by Tom Lehmann and published by Rio Grande Games. This implementation is created for educational and compatibility purposes.
