import os
from dotenv import load_dotenv
import anthropic

load_dotenv()
MODEL = "claude-sonnet-4-5-20250929"
client = anthropic.Anthropic()


# ---------------------
# TOOLS the agent can use
# ---------------------

TOOLS = [
    {
        "name": "calculator",
        "description": "Performs arithmetic calculations. Use for any math.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate, e.g. '25 * 48'"
                }
            },
            "required": ["expression"]
        }
    },
    {
        "name": "final_answer",
        "description": "Use this when you have the final answer to give to the user.",
        "input_schema": {
            "type": "object",
            "properties": {
                "answer": {
                    "type": "string",
                    "description": "The final answer to the user's question"
                }
            },
            "required": ["answer"]
        }
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Actually run the tool and return result."""
    
    if tool_name == "calculator":
        expr = tool_input["expression"]
        result = eval(expr)  # Simple for now (don't use eval in production!)
        return f"Result: {result}"
    
    elif tool_name == "final_answer":
        return tool_input["answer"]
    
    else:
        return f"Unknown tool: {tool_name}"

def run_agent(user_query: str) -> str:
    """
    Minimal ReAct agent loop.
    """
    
    print(f"\n{'='*50}")
    print(f"User Query: {user_query}")
    print(f"{'='*50}\n")
    
    # Conversation history
    messages = [
        {"role": "user", "content": user_query}
    ]
    
    system_prompt = """You are a helpful assistant that solves problems step by step.

When you need to calculate something, use the calculator tool.
When you have the final answer, use the final_answer tool.

Always think through the problem before acting."""

    # The agent loop
    while True:
        # THINK + decide on ACTION
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=system_prompt,
            tools=TOOLS,
            messages=messages
        )
        
        print(f"Stop reason: {response.stop_reason}")
        
        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            # Find the tool use block
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id
                    
                    print(f"TOOL CALL: {tool_name}")
                    print(f"INPUT: {tool_input}")
                    
                    # EXECUTE the tool
                    result = execute_tool(tool_name, tool_input)
                    print(f"RESULT: {result}")
                    
                    # Check if it's the final answer
                    if tool_name == "final_answer":
                        return result
                    
                    # Add assistant response + tool result to history
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use_id,
                            "content": result
                        }]
                    })
        
        else:
            # No tool use, Claude just responded with text
            # (Shouldn't happen with our setup, but handle it)
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text



if __name__ == "__main__":
    run_agent("I have 15 apples. I give away 7, then buy 3 times as many as I have left. How many do I have now?")
