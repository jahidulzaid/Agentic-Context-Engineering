import os

from pydantic import BaseModel, Field


class Config(BaseModel):
    agent_dir: str = os.path.dirname(os.path.abspath(__file__)) + "/agents"
    serve_web_interface: bool = True
    reload_agents: bool = True

    # Model configuration
    generator_model: str = Field(default="gemini-2.5-flash")
    reflector_model: str = Field(default="gemini-2.5-flash")
    curator_model: str = Field(default="gemini-2.5-flash")
    
    # Server configuration
    app_title: str = Field(default="ACE-ADK: Agentic Context Engineering")
    app_version: str = Field(default="0.1.0")
    server_host: str = Field(default="0.0.0.0")
    server_port: int = Field(default=8080)
