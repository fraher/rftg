## GENERAL
This repository contains the original C implementation of [Race for the Galaxy](https://boardgamegeek.com/boardgame/28143/race-galaxy) by [Tom Lehmann](http://boardgamegeek.com/boardgamedesigner/150/thomas-lehmann), originally developed by [Keldon Jones](http://keldon.net/rftg), and later improved by B. Nordli and J.-R. Reinhard.

## PYTHON PORT PROJECT
**This repository is currently being extended with a complete Python implementation located in the `python_rftg/` directory.**

### Project Goals
- Create an exact Python replica of the original C implementation
- Maintain 100% compatibility with save files, network protocols, and AI models
- Leverage modern Python features while preserving original game logic
- Enable easier modification, extension, and cross-platform deployment

### AI-Assisted Development Approach
This Python port is being developed using **specification-driven context engineering** with Claude 3.5 and Claude 4:

#### Methodology
1. **Comprehensive Specifications** ([`specifications.md`](specifications.md)): Complete technical documentation extracted from the C codebase, defining exact data structures, algorithms, protocols, and behaviors
2. **Task-Driven Development** ([`tasks.md`](tasks.md)): Structured implementation roadmap with checkpoints and validation requirements
3. **AI-Assisted Implementation**: Using Claude to systematically implement each component while ensuring specification compliance
4. **Continuous Validation**: Each implementation phase includes comprehensive testing against original behavior

#### Key Documents
- **[`specifications.md`](specifications.md)**: Technical specifications serving as ground truth for all implementations
- **[`tasks.md`](tasks.md)**: Live project tracker with completion status and progress indicators
- **[`python_rftg/`](python_rftg/)**: Modern Python implementation with full type hints and test coverage

### Development Status
- ✅ **Foundation Complete**: Core engine, data structures, virtual environment, testing framework
- 🔄 **Current Phase**: Card system implementation and game phase logic
- 📋 **Progress Tracking**: See [`tasks.md`](tasks.md) for detailed status and next steps

### Original C Implementation
The original C implementation remains in the `src/` directory. To download a copy of the original program, go to the [downloads section](../../wiki/Downloads) of the wiki. See the [main page](../../wiki) of the wiki for more information.

This repository was uploaded to GitHub on April, 2016, and is based on B. Nordli's patch repository. Keldon's original versions are included in the '[keldon](../../tree/keldon)' branch, as single commits attributed to Keldon Jones.

## TECHNICAL APPROACH

### Specification-Driven Development
Our Python port follows a rigorous **specification-first methodology**:

1. **Complete Analysis**: The original C codebase was thoroughly analyzed to extract every technical detail
2. **Formal Specifications**: All data structures, algorithms, protocols, and behaviors documented in [`specifications.md`](specifications.md)
3. **Exact Replication**: Python implementation matches C behavior precisely, including edge cases and quirks
4. **Validation Testing**: Every component tested against original behavior to ensure compatibility

### AI-Context Engineering
We're using **Claude 3.5 Sonnet** and **Claude 4** to systematically implement the Python port:

#### Process
- **Context Injection**: Specifications and task lists provide complete context for each implementation phase
- **Iterative Development**: Each component built incrementally with immediate testing and validation
- **Quality Assurance**: AI assists with code review, testing, and specification compliance checking
- **Documentation**: All code includes comprehensive type hints, docstrings, and specification references

#### Benefits
- **Consistency**: AI ensures uniform coding patterns and specification adherence
- **Completeness**: Systematic approach prevents missing edge cases or features
- **Quality**: Continuous validation and testing throughout development
- **Speed**: Rapid implementation while maintaining high quality standards

### Project Structure
```
rftg/
├── src/                    # Original C implementation
├── python_rftg/           # New Python implementation
│   ├── src/core/          # Core game engine (✅ Complete)
│   ├── tests/             # Test suite (✅ 15/15 passing)
│   ├── venv/              # Virtual environment
│   └── requirements.txt   # Dependencies
├── specifications.md      # Technical specifications (Ground truth)
├── tasks.md              # Project tracker (Live status)
└── readme.md             # This file
```

**Quick Links**: [`specifications.md`](specifications.md) | [`tasks.md`](tasks.md) | [`python_rftg/`](python_rftg/)

## LEGAL
The original game Race for the Galaxy is designed by Tom Lehmann and published by Rio Grande Games.

The source code is copyrighted and is placed under the GNU General Public License, version 2 (GPLv2). For details, see the file [COPYING](src/COPYING).

Rio Grande Games holds the copyrights for the images. Permission to distribute the card and goal images has been granted by Rio Grande Games. The image files may not be unpacked or redistributed without this notice, or used for any other purpose.

## GETTING STARTED

### Python Implementation
To work with the Python port:

```bash
# Navigate to the Python implementation
cd python_rftg

# Activate the virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Run tests to verify setup
python dev.py test

# Run the current implementation
python dev.py run
```

**See also**: [`python_rftg/README.md`](python_rftg/README.md) for detailed Python implementation documentation.

### Development
For development and contributing to the Python port:

1. **Review Specifications**: Read [`specifications.md`](specifications.md) for technical details
2. **Check Progress**: See [`tasks.md`](tasks.md) for current status and next tasks
3. **Run Tests**: Ensure all tests pass before making changes
4. **Follow Standards**: Use type hints, docstrings, and maintain specification compliance

### Original C Implementation
For the original C implementation, see [README](src/README).

## CONTRIBUTING

The Python port welcomes contributions! Please:

1. Review the specifications in [`specifications.md`](specifications.md)
2. Check current tasks and progress in [`tasks.md`](tasks.md)
3. Ensure all tests pass and new features include tests
4. Maintain exact compatibility with original behavior
5. Use comprehensive type hints and documentation

**Key Resources**: [`specifications.md`](specifications.md) | [`tasks.md`](tasks.md) | [`python_rftg/`](python_rftg/)

## README
For more information, see [README](src/README).
