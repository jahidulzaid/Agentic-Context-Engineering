from typing import AsyncGenerator

from google.adk.agents import Agent, BaseAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.genai.types import Part, UserContent
from pydantic import BaseModel, Field

from config import Config

config = Config()


# -------------------------
# 1) Generator output schema
# -------------------------
class GeneratorOutput(BaseModel):
    reasoning: list[str] = Field(
        description="Provide step-by-step reasoning process in the format of [step-by-step thought process / reasoning process / detailed analysis and calculation]"
    )
    bullet_ids: list[str] = Field(
        default_factory=list, description="List of playbook bullet IDs referenced"
    )
    final_answer: str = Field(description="Concise final answer")


# ============================================
# Generator: Generate answers and traces using playbook
# ============================================
generator_ = Agent(
    name="Generator",
    model=config.generator_model,
    description="Generates high-quality answers by applying strategies from the learned playbook. References specific tactics and avoids known pitfalls.",
    instruction="""
Your task is to answer user queries while providing structured step-by-step reasoning and the bullet IDs you used.

Input:
- User Query: {user_query}
- Current Playbook: {app:playbook}

【Required Guidelines】

1. Carefully read the playbook and apply relevant strategies, formulas, and insights
   - Check all bullet points in the playbook
   - Understand the context and application conditions of each strategy

2. Carefully examine common failures (anti-patterns) listed in the playbook and avoid them
   - Present specific alternatives or best practices

3. Show the reasoning process step by step
   - Clearly indicate which bullets you referenced at each stage
   - Structure so that the logic flow is clear

4. Create thorough but concise analysis
   - Include only essential information, but include all central evidence
   - Avoid unnecessary repetition

5. Review calculations and logic before providing the final answer
   - Confirm that all referenced bullet_ids were actually used
   - Check for logical contradictions
   - Double-check that you haven't missed any relevant playbook bullets

【Output Rules】
- reasoning: Step-by-step thought process (step-by-step chain of thought), detailed analysis and calculations
- bullet_ids: List of referenced playbook bullet IDs
- final_answer: Clear and verified final answer
""",
    include_contents="none",  # Focus on state value injection
    output_schema=GeneratorOutput,  # Structure output
    output_key="generator_output",  # Save to session.state['generator_output']
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)


class FinalAnswerDisplay(BaseAgent):
    """Display the final answer prominently to the user."""
    
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        state = ctx.session.state
        generator_output: dict | None = state.get("generator_output")
        
        if not generator_output:
            yield Event(
                author=self.name,
                invocation_id=ctx.invocation_id,
                content=UserContent(
                    parts=[Part(text="No answer generated.")]
                ),
            )
            return
        
        output = GeneratorOutput.model_validate(generator_output)
        
        # Create a beautifully formatted final answer display
        answer_display = f"""
╔══════════════════════════════════════════════════════════════╗
║                      FINAL ANSWER                            ║
╚══════════════════════════════════════════════════════════════╝

{output.final_answer}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Reasoning Steps: {len(output.reasoning)}
Playbook Bullets Used: {len(output.bullet_ids)}
{f"Referenced: {', '.join(output.bullet_ids[:5])}" if output.bullet_ids else ""}
{f"   ... and {len(output.bullet_ids) - 5} more" if len(output.bullet_ids) > 5 else ""}
"""
        
        content = UserContent(parts=[Part(text=answer_display)])
        
        yield Event(
            author=self.name,
            invocation_id=ctx.invocation_id,
            content=content,
        )


final_answer_display = FinalAnswerDisplay(
    name="final_answer_display",
    description="Displays the final answer prominently to the user."
)


# Wrap generator with final answer display
generator = SequentialAgent(
    name="Generator",
    description="Generates answers and displays the final result prominently.",
    sub_agents=[generator_, final_answer_display],
)

