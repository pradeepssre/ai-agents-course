Agent = LLM in a loop that can take actions
The loop: Observe → Think → Act → Repeat
ReAct = Reasoning + Acting (Thought → Action → Observation)

┌─────────────────────────────────────┐
│                                     │
│   ┌─────────┐                       │
│   │ OBSERVE │ ← get input/results   │
│   └────┬────┘                       │
│        ▼                            │
│   ┌─────────┐                       │
│   │  THINK  │ ← reason about it     │
│   └────┬────┘                       │
│        ▼                            │
│   ┌─────────┐                       │
│   │   ACT   │ ← use a tool OR       │
│   └────┬────┘   give final answer   │
│        │                            │
│        ▼                            │
│   Done? ──No──► loop back           │
│     │                               │
│    Yes                              │
│     ▼                               │
│   Return answer                     │
│                                     │
└─────────────────────────────────────┘


The ReAct Pattern
ReAct = Reasoning + Acting
The LLM explicitly says:

Thought: "I need to find Datadog's pricing..."
Action: search("Datadog pricing")
Observation: [search results come back]
Thought: "Now I have the pricing, I can answer..."
Action: final_answer("Datadog costs $15/host/month...")

The magic: the LLM's reasoning is visible, not a black box.

Why This Matters
Without agents:

User: "What's Datadog's current pricing?"
LLM: "Based on my training data from 2024..." ❌ (stale)

With agents:

User: "What's Datadog's current pricing?"
LLM: thinks → searches web → reads results → "As of today, Datadog costs..." ✅


