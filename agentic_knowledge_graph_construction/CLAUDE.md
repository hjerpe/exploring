# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Environment Setup

### Package Management
- Use `uv` for Python package management and virtual environments
- Install dependencies: `uv sync` or `uv pip install -r requirements.txt`
- Activate environment: `uv shell` or use `uv run` for commands

### Environment Variables
- Configure Neo4j connection settings in `.env` file:
  - `NEO4J_URI`: Neo4j database URI (default: bolt://localhost:7687)
  - `NEO4J_USERNAME`: Database username (default: neo4j)
  - `NEO4J_PASSWORD`: Database password (default: password)
  - `NEO4J_DATABASE`: Database name (default: KGS_FOR_RAG)

## Common Commands

### Development Setup
```bash
# Install dependencies with uv
uv sync

# Run commands in the uv environment
uv run python script.py
uv run jupyter notebook
```

### Code Quality
```bash
# Run pre-commit hooks (black, isort, pycln, nbstripout)
pre-commit run --all-files

# Type checking
mypy .
```

### Docker Environment
```bash
# Use devcontainer for development with Neo4j
# Open in VS Code with Dev Containers extension
```

## Project Architecture

### Core Components
- **Neo4j Integration**: Knowledge graph database setup and querying capabilities via LangChain
- **Jupyter Notebooks**: Interactive development environment for knowledge graph exploration
- **Docker Support**: Containerized development environment with Neo4j database

### Directory Structure
- `notebook/`: Jupyter notebooks for knowledge graph querying and analysis
- `.devcontainer/`: VS Code development container configuration with Docker Compose
- `neo4j_db/`: Neo4j database files and configuration

### Key Dependencies
- `langchain-community`: For Neo4j graph integration
- `neo4j`: Neo4j Python driver
- `python-dotenv`: Environment variable management
- `click`: Command-line interface for utilities
- `pyyaml`: YAML file parsing

### Development Workflow
1. Use `uv` to manage Python dependencies and environment
2. Configure Neo4j connection in `.env` file
3. Use Jupyter notebooks in `notebook/` directory for interactive development
4. Run pre-commit hooks before committing changes
5. Use Docker devcontainer for consistent development setup
