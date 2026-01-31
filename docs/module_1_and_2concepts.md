# Module 2: Tool Use Deep Dive - Complete Reference

## Understanding LLM Tool Calling Mechanics

This document provides a comprehensive understanding of how tool use works with Claude's API, covering the complete flow from request to response, error handling, and optimization strategies.

---

## Part 1: What Actually Happens When You Call Claude with Tools?

### Your Request to Claude

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant...",
    tools=TOOLS,  # ← This is key!
    messages=[
        {"role": "user", "content": "What is Datadog's pricing?"}
    ]
)
```

**What's happening:**
1. You're sending Claude your tool **definitions** (schemas)
2. Claude analyzes: "What tools do I have available?"
3. Claude reasons: "To answer this, I need current info → I should use `web_search`"

---

### Claude's Response Structure

Claude returns a `Message` object with this structure:

```python
{
    "id": "msg_01ABC123...",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "I'll search for Datadog's pricing information."
        },
        {
            "type": "tool_use",
            "id": "toolu_01XYZ789...",  # ← Important! You need this ID
            "name": "web_search",
            "input": {
                "query": "Datadog infrastructure monitoring pricing"
            }
        }
    ],
    "stop_reason": "tool_use",  # ← This tells you why Claude stopped
    "usage": {
        "input_tokens": 450,
        "output_tokens": 89
    }
}
```

**Key observations:**

1. **`content` is an ARRAY**: Can contain multiple blocks
2. **Block types**: `text` OR `tool_use` (can have both!)
3. **`tool_use` structure:**
   - `id`: Unique identifier (you MUST include this in your response)
   - `name`: Which tool Claude wants to use
   - `input`: The arguments Claude generated
4. **`stop_reason`**: 
   - `"tool_use"` = Claude wants to use a tool
   - `"end_turn"` = Claude is done, no tools needed
   - `"max_tokens"` = Hit token limit (potential issue)

---

### Your Tool Result Back to Claude

After you execute the tool, you send results back:

```python
messages.append({
    "role": "assistant",
    "content": response.content  # ← The ENTIRE content array with tool_use
})

messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": "toolu_01XYZ789...",  # ← MUST match the tool_use id!
            "content": "Search results: [Datadog pricing starts at $15/host/month...]"
        }
    ]
})
```

**Critical points:**

1. **You must include the assistant's full response** (with the `tool_use` block) in messages
2. **Then append the tool results** as a user message
3. **`tool_use_id` MUST match** - this is how Claude knows which tool call this result corresponds to

---

## Part 2: Multiple Tool Uses (Parallel Execution)

This is where it gets interesting! Claude can request **multiple tools at once**.

### Example: Claude's Response with Multiple Tools

```python
{
    "content": [
        {
            "type": "text",
            "text": "I'll search for both competitors to compare them."
        },
        {
            "type": "tool_use",
            "id": "toolu_01AAA",
            "name": "web_search",
            "input": {"query": "Datadog pricing"}
        },
        {
            "type": "tool_use",
            "id": "toolu_01BBB",
            "name": "web_search",
            "input": {"query": "Splunk pricing"}
        }
    ],
    "stop_reason": "tool_use"
}
```

### Your Code Must Handle This

```python
# Collect ALL tool results
tool_results = []

for block in response.content:
    if block.type == "tool_use":
        result = execute_tool(block.name, block.input)
        tool_results.append({
            "type": "tool_result",
            "tool_use_id": block.id,  # Each has unique ID
            "content": result
        })

# Send ALL results back at once
messages.append({"role": "assistant", "content": response.content})
messages.append({
    "role": "user",
    "content": tool_results  # ← Array of tool_result objects
})
```

**Why this matters:**
- Parallel execution is **faster** and more **efficient**
- Claude can gather multiple pieces of info simultaneously
- Your code must collect ALL results before responding

---

## Part 3: The Complete Agent Loop - Message Flow

Let me trace a complete example with actual message history:

### User Query
```
"Compare Datadog and Splunk pricing for 100 servers"
```

### Turn 1 - Initial Messages

```python
[
    {
        "role": "user",
        "content": "Compare Datadog and Splunk pricing for 100 servers"
    }
]
```

### Turn 1 - Claude's Response

```python
# Claude decides to search for both
{
    "content": [
        {"type": "text", "text": "I'll search for both products' pricing."},
        {"type": "tool_use", "id": "tool_A", "name": "web_search", "input": {"query": "Datadog pricing"}},
        {"type": "tool_use", "id": "tool_B", "name": "web_search", "input": {"query": "Splunk pricing"}}
    ],
    "stop_reason": "tool_use"
}
```

### Turn 1 - After Tool Execution, Messages Become

```python
[
    {
        "role": "user",
        "content": "Compare Datadog and Splunk pricing for 100 servers"
    },
    {
        "role": "assistant",
        "content": [
            {"type": "text", "text": "I'll search for both products' pricing."},
            {"type": "tool_use", "id": "tool_A", "name": "web_search", "input": {...}},
            {"type": "tool_use", "id": "tool_B", "name": "web_search", "input": {...}}
        ]
    },
    {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": "tool_A", "content": "Datadog results..."},
            {"type": "tool_result", "tool_use_id": "tool_B", "content": "Splunk results..."}
        ]
    }
]
```

### Turn 2 - Claude's Response

```python
# Claude now has pricing info but needs to scrape details
{
    "content": [
        {"type": "text", "text": "Let me get detailed pricing from their pages."},
        {"type": "tool_use", "id": "tool_C", "name": "web_scrape", "input": {"url": "https://datadog.com/pricing"}},
        {"type": "tool_use", "id": "tool_D", "name": "web_scrape", "input": {"url": "https://splunk.com/pricing"}}
    ],
    "stop_reason": "tool_use"
}
```

### Turn 2 - After Scraping, Messages Become

```python
[
    # ... previous messages ...
    {
        "role": "assistant",
        "content": [
            {"type": "text", "text": "Let me get detailed pricing from their pages."},
            {"type": "tool_use", "id": "tool_C", ...},
            {"type": "tool_use", "id": "tool_D", ...}
        ]
    },
    {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": "tool_C", "content": "Datadog: $15/host/month..."},
            {"type": "tool_result", "tool_use_id": "tool_D", "content": "Splunk: $150/GB..."}
        ]
    }
]
```

### Turn 3 - Claude's Response

```python
# Now Claude can calculate
{
    "content": [
        {"type": "text", "text": "Let me calculate the costs for 100 servers."},
        {"type": "tool_use", "id": "tool_E", "name": "calculator", "input": {"expression": "15 * 100 * 12"}}
    ],
    "stop_reason": "tool_use"
}
```

### Turn 4 - Claude's Final Response

```python
# After calculator result
{
    "content": [
        {"type": "text", "text": "Based on my research:\n\nDatadog: $18,000/year...\nSplunk: Varies based on data volume...\n\nDatadog is more predictable for infrastructure monitoring."}
    ],
    "stop_reason": "end_turn"  # ← No more tools needed!
}
```

---

## Part 4: Stop Reasons - What They Mean

| Stop Reason | Meaning | What You Do |
|-------------|---------|-------------|
| `"tool_use"` | Claude wants to use tool(s) | Execute tools, send results back, continue loop |
| `"end_turn"` | Claude is done responding | Extract text response, end loop |
| `"max_tokens"` | Hit token limit | Possible issue - might need higher max_tokens |
| `"stop_sequence"` | Hit custom stop sequence | Rare - only if you defined stop sequences |

---

## Part 5: Error Handling - What Can Go Wrong?

### Error 1: Tool Execution Fails

```python
def execute_tool(tool_name: str, tool_input: dict) -> str:
    try:
        if tool_name == "web_search":
            # API call fails
            result = tavily_client.search(query)
    except Exception as e:
        # Return error as string - Claude can handle this!
        return f"Error: {str(e)}"
```

**Key principle:** NEVER raise exceptions from tool execution. Always return a string describing the error. Claude can reason about errors and try alternatives!

### Error 2: Mismatched `tool_use_id`

```python
# ❌ WRONG - ID doesn't match
messages.append({
    "role": "user",
    "content": [{
        "type": "tool_result",
        "tool_use_id": "wrong_id",  # Doesn't match Claude's tool_use.id
        "content": "..."
    }]
})
```

**Result:** API error - "tool_use_id not found"

### Error 3: Missing Tool Results

```python
# ❌ WRONG - Claude called 2 tools, you only returned 1 result
# Claude called: tool_A and tool_B
# You only return result for tool_A
```

**Result:** API error - missing tool results

---

## Part 6: Token Economics - The Cost Model

Every API call has costs:

```python
response.usage = {
    "input_tokens": 1250,   # Your prompt + tools + message history
    "output_tokens": 180    # Claude's response
}
```

### What Counts as Input Tokens?

1. Your system prompt
2. ALL tool definitions (your entire `TOOLS` array)
3. Entire conversation history (all messages)
4. Current user message

### What Counts as Output Tokens?

1. Claude's text response
2. Claude's tool_use blocks (the JSON for tool calls)

### Cost Implications

```python
# With 4 tools defined
Tool definitions ≈ 400 tokens (per call)

# After 5 turns of conversation
Message history ≈ 2000 tokens (growing)

# Each tool result
Tool result ≈ 200-1000 tokens (depends on size)
```

### Optimization Strategies

1. **Tool result truncation**: Don't return entire web pages
2. **Message summarization**: After many turns, summarize history
3. **Selective tool definitions**: Only include tools needed for current task
4. **Efficient tool results**: Structured data instead of prose

---

## Part 7: Schema Design - Why It Matters

Let's compare two schemas for the same tool:

### Bad Schema

```python
{
    "name": "search",
    "description": "Search",
    "input_schema": {
        "type": "object",
        "properties": {
            "q": {"type": "string"}
        },
        "required": ["q"]
    }
}
```

**Problems:**
- Vague description ("Search" - search what? when to use?)
- Unclear parameter name ("q" - what should I put here?)
- No guidance on format

**Result:** Claude might misuse this tool or not use it when appropriate.

### Good Schema

```python
{
    "name": "web_search",
    "description": "Search the internet for current information about companies, products, pricing, features, or market trends. Use this when you need information not in your training data or when the user asks about recent events. Returns titles, URLs, and content snippets from relevant web pages.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query. Be specific and include key terms like company names, product names, or concepts. Example: 'Datadog infrastructure monitoring pricing 2024'"
            },
            "max_results": {
                "type": "integer",
                "description": "Number of results to return. Use 3-5 for focused queries, 8-10 for broader research.",
                "minimum": 1,
                "maximum": 10,
                "default": 5
            }
        },
        "required": ["query"]
    }
}
```

**Improvements:**
- **Clear when to use**: "current information", "not in training data"
- **Examples**: Shows Claude exactly what to put
- **Constraints**: `minimum`, `maximum`, `default`
- **Guidance**: "3-5 for focused queries"

**Result:** Claude uses the tool more accurately and effectively.

---

## Part 8: The `final_answer` Pattern - Why It's Useful

### The Pattern

```python
{
    "name": "final_answer",
    "description": "Use this when you have the final answer to give to the user.",
    "input_schema": {
        "type": "object",
        "properties": {
            "answer": {"type": "string", "description": "The final answer"}
        },
        "required": ["answer"]
    }
}
```

### Without `final_answer`

```python
if response.stop_reason == "end_turn":
    # Extract text from response
    for block in response.content:
        if block.type == "text":
            return block.text
```

**Problem:** Ambiguous - is Claude done, or just thinking out loud?

### With `final_answer`

```python
if tool_name == "final_answer":
    return tool_input["answer"]  # Definitive end!
```

### Benefits

1. **Explicit termination**: Claude explicitly signals "I'm done"
2. **Structured output**: The answer is in a known field
3. **Forces completion**: Claude must consciously finish
4. **Clear in logs**: You can see when Claude decided to finish

**This is a production-grade pattern!** Many agent frameworks use variations of this.

---

## Key Takeaways for Module 2

1. **Tool use is a conversation**: You send tools → Claude requests → You execute → Claude synthesizes

2. **Content is an array**: Always iterate through `response.content` - it can have multiple blocks

3. **IDs must match**: `tool_use_id` in results must match `tool_use.id` from Claude's request

4. **Parallel is powerful**: Claude can request multiple tools simultaneously - your code must handle it

5. **Errors are data**: Return errors as strings, don't raise exceptions - let Claude adapt

6. **Schemas are UX**: Your tool descriptions are Claude's interface - invest in good descriptions

7. **Tokens add up**: Every tool call, every result, every message adds tokens - optimize!

8. **Stop reasons guide flow**: Check `stop_reason` to know what to do next

---

## Critical Thinking Questions

Before implementing Module 2, consider these questions:

1. **When should Claude use web_search vs. web_scrape?** How would you describe this in the tool schemas?

2. **What happens if a scrape fails?** Should Claude retry with a different URL? How would it know to do that?

3. **How do you prevent tool result bloat?** If a web page is 50,000 characters, what do you return?

4. **Should save_note return anything useful?** Or just confirmation? What if the user asks "what have we researched about Datadog?"

5. **How many parallel tool calls is too many?** What if Claude tries to search for 10 competitors at once?

---

## Production Patterns Checklist

When building tools for production, ensure:

- [ ] Tool descriptions clearly explain WHEN to use the tool
- [ ] Parameter descriptions include examples
- [ ] All tool execution is wrapped in try-except
- [ ] Errors return descriptive strings, not exceptions
- [ ] Tool results are truncated to reasonable sizes
- [ ] Multiple tool results are collected before sending back
- [ ] `tool_use_id` matching is correct
- [ ] Stop reasons are properly handled
- [ ] Token usage is monitored
- [ ] Tool definitions only include what's needed

---

*End of Module 2 Deep Dive Reference*