from dotenv import load_dotenv
import anthropic
load_dotenv()

import requests

from tavily import TavilyClient
MODEL = "claude-sonnet-4-5-20250929"
client = anthropic.Anthropic()
tavily_client = TavilyClient()


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
    },
    {
        "name": "web_search",
        "description": "Use this tool to search the web for information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "currency_convertor",
        "description": "Use this tool to convert an amount from one currency to the other.",
        "input_schema": {
            "type": "object",
            "properties": {
               
               "amount" : {
                "type": "number",
                "description" : "the amount that needs to be converted"
               },
               "from_currency" :{
                "type" : "string",
                "description" : "The source currency code eg INR,USD,EUR,JPY"
               },
               "to_currency":{
                "type" : "string",
                "description" : "The target currency code eg INR,USD,EUR,JPY"
               }
            },
            "required": ["amount","from_currency","to_currency"]
        }
    }
]

def currency_convertor_tool(amount:float,from_currency:str,to_currency:str) -> str : 
    """Convert currency using frankfurter.app API"""
    try:
        if amount<=0 : 
            return "Error: Amount must be greater than 0"
        if len(from_currency)!= 3:
            return "Error: From currency code must be 3 characters"
        if len(to_currency)!= 3:
            return "Error: To currency code must be 3 characters"
        
        # call API 
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        url = f'https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}'
        response = requests.get(url, timeout=5)

        if response.status_code == 200 : 
            data = response.json()
            converted = data['rates'][to_currency]
            return f"{amount} {from_currency} = {converted:.2f} {to_currency} (Rate: {converted/amount:.4f})"
        else : 
            return f"Error: API returned status {response.status_code}"
    
    except requests.Timeout:
        return "Error: Currency API request timed out"
    except KeyError:
        return f"Error: Invalid currency code. {from_currency} or {to_currency} may not be supported"
    except Exception as e:
        return f"Error converting currency: {str(e)}"



def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Actually run the tool and return result."""
    
    if tool_name == "calculator":
        expr = tool_input["expression"]
        result = eval(expr)  # Simple for now (don't use eval in production!)
        return f"Result: {result}"
    
    elif tool_name == "final_answer":
        return tool_input["answer"]
    
    elif tool_name == "web_search":
        query = tool_input["query"]
        results = tavily_client.search(query, max_results=5)  # Note: it's max_results, not num_results
        # Format the results as a string
        formatted = []
        
        # Add the AI summary if available
        if results.get('answer'):
            formatted.append(f"Summary: {results['answer']}\n")
        
        # Add individual results
        formatted.append("Search Results:")
        for i, result in enumerate(results.get('results', []), 1):
            formatted.append(f"\n{i}. {result.get('title', 'No title')}")
            formatted.append(f"   {result.get('content', '')[:200]}...")
            formatted.append(f"   URL: {result.get('url', '')}")
        
        return "\n".join(formatted) 
    elif tool_name=="currency_convertor":
        return currency_convertor_tool(
            amount = tool_input['amount'],
            from_currency = tool_input['from_currency'],
            to_currency = tool_input['to_currency']
        )
    
    else:
        return f"Unknown tool: {tool_name}"

# def run_agent(user_query: str) -> str:
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
When you need to search the web, use the web_search tool.
When you need to convert currency, use the currency_convertor tool.
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
            tool_results = []
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
                    
                    tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use_id,
                "content": result
            })
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
When you need to search the web, use the web_search tool.
When you need to convert currency, use the currency_convertor tool.
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
            tool_results = []  # Collect ALL tool results here
            
            # Process each tool use
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
                    
                    # Add to results list
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result
                    })
            
            # Add messages ONCE after processing ALL tools
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": tool_results
            })
        
        else:
            # No tool use, Claude just responded with text
            for block in response.content:
                if hasattr(block, "text"):
                    return block.text


if __name__ == "__main__":
    run_agent("I have 10 apples. I give away 7, then buy 2 times as many as I have left. How many do I have now? Once you get the result assume this as the amount in USD and convert it to British Pounds")
