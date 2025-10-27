# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-28

### Added
- Initial release of ACE-ADK (Agentic Context Engineering - Agent Development Kit)
- Sequential agent architecture with three specialized agents:
  - **Generator**: Creates answers using learned playbook strategies
  - **Reflector**: Analyzes outputs and tags helpful/harmful insights
  - **Curator**: Updates the playbook with new learnings
- Self-improving system that learns from each interaction
- Transparent reasoning with step-by-step thought process display
- Context-aware playbook management system
- Quality-focused feedback loop (identifies what works and what doesn't)
- Final answer display component with ASCII box formatting
- Cycle summary component showing complete iteration statistics
- FastAPI web interface with custom splash screen
- Google ADK integration with Gemini 2.5 Flash model
- Comprehensive error handling for JSON parsing and validation
- Output limiting to prevent token overflow
- State management across agent iterations
- Configuration management via environment variables

### Features
- **Web Interface**: http://localhost:8080 with dev UI
- **API Documentation**: Auto-generated at /docs endpoint
- **Multi-Model Support**: Configurable LLM models for each agent
- **Playbook System**: Dynamic knowledge base that evolves over time
- **Bullet Tagging**: Automatic categorization of helpful/harmful insights
- **Delta Operations**: Add, update, delete operations for playbook management

### Technical
- Python 3.13+ support
- Google ADK v1.16.0+
- FastAPI + uvicorn web server
- Pydantic v2 for data validation
- Environment-based configuration
- GitHub Actions CI/CD workflow
- Comprehensive requirements.txt
- Professional README with setup guide

### Configuration
- Customizable server host and port
- Flexible model selection per agent
- Agent directory configuration
- Web interface toggle
- Hot reload support for development

### Documentation
- Complete README with installation instructions
- Architecture overview and agent workflow
- Configuration guide with examples
- Troubleshooting section
- API usage examples
- Contributing guidelines

### CI/CD
- GitHub Actions workflow for testing
- Python syntax validation
- Import verification
- Security scanning
- Docker build support
- Multi-version Python testing (3.13+)

[0.1.0]: https://github.com/jahidulzaid/Agentic-Context-Engineering/releases/tag/v0.1.0
