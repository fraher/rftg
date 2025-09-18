# Alternate Approaches for Card Data Loading

This document surveys multiple strategies for replacing the temporary `_create_test_cards()` placeholder in `GameEngine` with a production-ready card data loading pipeline. Each approach is evaluated on its compatibility with the original C implementation, maintainability, performance characteristics, and testing implications.

## Evaluation Criteria

| Criterion | Description |
| --- | --- |
| **Specification Fidelity** | How well the approach preserves the card definitions from the original C data files. |
| **Runtime Performance** | Relative cost of loading card data when a new game starts. |
| **Tooling & Maintenance** | Complexity of updating card definitions, adding expansions, or fixing data bugs. |
| **Testing Support** | Ease of injecting fixtures, validating integrity, and supporting deterministic test data. |

## Approach 1: Precompiled Static Data Files

**Summary:** Convert the original C card tables into neutral data files (JSON, YAML, or TOML) as part of the build process and ship the generated artifacts with the Python package.

- **Workflow**
  1. Author a one-time conversion script in `tools/` that parses the C arrays and exports normalized records.
  2. Store the generated files under `python_rftg/resources/cards/` and load them with `importlib.resources`.
  3. Validate the files during CI to ensure they remain in sync with the canonical C source.
- **Advantages**
  - Fast startup: the engine reads ready-to-use serialized data.
  - Human-readable artifacts simplify audits and community contributions.
  - Compatible with packaging (wheels, installers) without extra dependencies.
- **Trade-offs**
  - Requires a regeneration step whenever the C tables change.
  - Risk of drift if the conversion script is not executed as part of CI.
- **Testing Implications**
  - Fixtures can reuse the serialized files or load slimmed-down variants for targeted scenarios.
  - Schema validation can be performed with JSON Schema or `pydantic` models to catch data regressions.

## Approach 2: Direct Parsing of the Original Assets

**Summary:** Load the card definitions directly from the original resources (C headers, binary blobs, or compiled data files) at runtime to guarantee byte-for-byte fidelity.

- **Workflow**
  1. Use `ctypes`, `cffi`, or structured binary parsers (`construct`) to interpret the original data formats.
  2. Map the parsed structures to the Python `Design` and `Power` dataclasses.
  3. Cache the parsed data to avoid repeated I/O in long-running sessions.
- **Advantages**
  - Ensures absolute parity with the C implementation, removing translation risk.
  - Simplifies expansion support because new official assets drop in automatically.
- **Trade-offs**
  - Increases runtime dependencies and complexity (FFI bindings, binary parsers).
  - Harder to reason about for contributors unfamiliar with the legacy layout.
  - Startup time is slower because parsing happens on demand.
- **Testing Implications**
  - Golden master tests can compare parsed data against hashes from the C build pipeline.
  - Unit tests may need mock layers to avoid platform-specific binary access.

## Approach 3: Structured Data Store (SQLite or DuckDB)

**Summary:** Store card metadata, counts, and expansion flags in an embedded database populated during installation or the build process.

- **Workflow**
  1. Define normalized tables (`designs`, `powers`, `expansions`, `localization`).
  2. Populate the database using the original C definitions or curated spreadsheets.
  3. Use lightweight ORM helpers (e.g., `dataclasses`, `sqlite3.Row`) to hydrate engine objects.
- **Advantages**
  - Provides strong querying, filtering, and localization support for future UI tooling.
  - Facilitates analytics (e.g., balance checks, AI training data exports).
  - Schema migrations can track historical changes across expansions.
- **Trade-offs**
  - Adds an extra artifact to package and version.
  - Requires migration tooling and version negotiation logic.
  - Overkill if the data set remains small and rarely changes.
- **Testing Implications**
  - In-memory SQLite databases allow fast fixtures and rollback-based tests.
  - Schema migrations must be tested to ensure backwards compatibility.

## Approach 4: Generated Python Modules

**Summary:** Auto-generate a strongly-typed Python module (e.g., `python_rftg/src/data/cards.py`) that instantiates `Design` objects at import time.

- **Workflow**
  1. Run a generator script that emits Python code with constant definitions and dataclass construction calls.
  2. Import the generated module from `GameEngine` to retrieve canonical `Design` instances.
  3. Expose helper functions for test overrides (e.g., `get_card_by_id`).
- **Advantages**
  - Zero runtime parsing overhead; the interpreter executes native Python objects.
  - Full type checking and IDE support because the objects exist as code.
  - Simplifies selective imports for unit tests or card filters.
- **Trade-offs**
  - Large generated files can be unwieldy to review and may trigger formatting lint rules.
  - Requires regeneration tooling similar to Approach 1.
  - Risk of merge conflicts when multiple contributors regenerate simultaneously.
- **Testing Implications**
  - Code generation can include checksum assertions to detect drift.
  - Static analyzers (mypy, pyright) can verify field coverage at build time.

## Comparison Matrix

| Approach | Fidelity | Performance | Maintenance | Testing |
| --- | --- | --- | --- | --- |
| Precompiled Files | High (with CI enforcement) | Fast | Moderate | Strong fixture support |
| Direct Parsing | Highest | Moderate to Slow | Complex | Requires mocks for isolation |
| Structured Store | High | Moderate | Higher | Excellent for integration testing |
| Generated Modules | High | Fastest | Moderate | Works well with static analysis |

## Recommendation

For the next development milestone, **Approach 1 (Precompiled Static Data Files)** strikes the best balance between fidelity, simplicity, and maintainability. It keeps the runtime lightweight, plays nicely with packaging, and can be backed by automated regeneration checks to prevent drift. Once the core Python port reaches feature parity, the team can re-evaluate whether the richer querying capabilities of Approaches 2 or 3 justify the additional complexity.

