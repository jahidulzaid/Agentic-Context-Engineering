import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from google.adk.cli.fast_api import get_fast_api_app

from config import Config

config = Config()

app: FastAPI = get_fast_api_app(
    agents_dir=config.agent_dir,
    web=config.serve_web_interface,
    reload_agents=config.reload_agents,
)

# Add custom metadata for better frontend display
app.title = "ACE-ADK: Agentic Context Engineering"
app.description = """
**Agentic Context Engineering - Agent Development Kit**

An intelligent agent system that learns and improves through iterative cycles:

### Agent Workflow:
1. **Generator** - Creates answers using learned playbook strategies
2. **Reflector** - Analyzes outputs and tags helpful/harmful insights  
3. **Curator** - Updates the playbook with new learnings

### Features:
- **Self-improving**: Learns from each interaction
- **Transparent reasoning**: Shows step-by-step thought process
- **Context-aware**: Maintains and evolves a knowledge playbook
- **Quality focused**: Identifies what works and what doesn't

### How to Use:
1. Ask any question or problem
2. Watch as the agent generates, reflects, and learns
3. See the playbook grow with insights over time

**Powered by Google ADK & Gemini 2.5 Flash**
"""
app.version = "0.1.0"

# Add a custom welcome endpoint
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ACE-ADK - Agentic Context Engineering</title>
        <meta http-equiv="refresh" content="0; url=/dev-ui/?app=ACE_Agent">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                text-align: center;
                padding: 40px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }
            h1 {
                font-size: 3em;
                margin: 0;
                animation: fadeIn 1s;
            }
            p {
                font-size: 1.2em;
                margin: 20px 0;
                animation: fadeIn 1.5s;
            }
            .loader {
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top: 4px solid white;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>ACE-ADK</h1>
            <p>Agentic Context Engineering</p>
            <div class="loader"></div>
            <p style="font-size: 0.9em;">Redirecting to interface...</p>
        </div>
    </body>
    </html>
    """


def main():
    print("\n" + "="*60)
    print("ACE-ADK: Agentic Context Engineering")
    print("="*60)
    print(f"Web Interface: http://localhost:{config.server_port}")
    print(f"API Docs: http://localhost:{config.server_port}/docs")
    print(f"Agent: ace_agent")
    print("="*60 + "\n")
    
    uvicorn.run(
        app, 
        host=config.server_host, 
        port=config.server_port,
        log_level="info"
    )


if __name__ == "__main__":
    main()
