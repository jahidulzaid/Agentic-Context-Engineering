from __future__ import annotations

from typing import AsyncGenerator

from google.adk.agents import BaseAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai.types import Part, UserContent

from .schemas.playbook import Playbook
from .sub_agents import curator, generator, reflector


class StateInitializer(BaseAgent):
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        state = ctx.session.state

        state_changes = {}
        state_changes["user_query"] = ctx.user_content

        # Required state
        # Initialize app:playbook
        if "app:playbook" not in state:
            pb = Playbook()
            state_changes["app:playbook"] = pb.to_dict()

        # 🔹 ground_truth (optional)
        # If user doesn't provide, explicitly initialize with None
        if "ground_truth" not in state:
            state_changes["ground_truth"] = None

        actions_with_update = EventActions(state_delta=state_changes)

        yield Event(
            author=self.name,
            invocation_id=ctx.invocation_id,
            actions=actions_with_update,
        )


state_initializer = StateInitializer(name="StateInitializer")


class CycleSummary(BaseAgent):
    """Display a summary of the complete ACE cycle."""
    
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        state = ctx.session.state
        
        # Get all outputs
        generator_output = state.get("generator_output", {})
        reflector_output = state.get("reflector_output", {})
        curator_output = state.get("curator_output", {})
        playbook = state.get("app:playbook", {})
        
        # Get final answer
        final_answer = generator_output.get("final_answer", "N/A") if generator_output else "N/A"
        
        # Get playbook stats
        playbook_obj = Playbook.from_dict(playbook) if playbook else None
        stats = playbook_obj.stats() if playbook_obj else {"sections": 0, "bullets": 0, "tags": {"helpful": 0, "harmful": 0, "neutral": 0}}
        
        # Get reflection insights
        key_insight = reflector_output.get("key_insight", "None") if reflector_output else "None"
        
        # Get curator changes
        operations = curator_output.get("operations", []) if curator_output else []
        num_operations = len(operations)
        
        summary = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{final_answer}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sections: {stats['sections']}
Total Bullets: {stats['bullets']}
Helpful Tags: {stats['tags']['helpful']}
Harmful Tags: {stats['tags']['harmful']}
Neutral Tags: {stats['tags']['neutral']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The playbook continues to evolve and improve with each interaction!
"""
        
        content = UserContent(parts=[Part(text=summary)])
        
        yield Event(
            author=self.name,
            invocation_id=ctx.invocation_id,
            content=content,
        )


cycle_summary = CycleSummary(name="cycle_summary", description="Displays a summary of the ACE cycle.")

# ============================================
# Orchestration: Generator → Reflector → Curator → Summary
# ============================================
ace_iteration = SequentialAgent(
    name="Context_Engineering_Agent",
    sub_agents=[
        state_initializer,
        generator,
        reflector,
        curator,
        cycle_summary,
    ],
    description="""ACE Agent: Agentic Context Engineering System

A self-improving agent that learns through iterative cycles:

- Generator: Answers questions using learned strategies
- Reflector: Analyzes quality and identifies improvements  
- Curator: Updates knowledge playbook with insights

Each interaction makes the agent smarter by building a playbook of proven strategies and avoiding past mistakes.
""",
)

root_agent = ace_iteration
