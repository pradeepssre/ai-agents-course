# AI Agents Mastery - Enhanced Learning Curriculum

## Learning System Overview

### Core Principles
1. **Quality over speed** - Understanding matters more than completion
2. **Build to learn** - Every concept is immediately implemented
3. **Incremental progress** - Small, testable pieces that work
4. **Retention through practice** - Mini-projects after each module
5. **Context continuity** - System to maintain learning state across sessions

---

## Teaching Methodology

### The "Concept → Build → Validate → Reflect" Cycle

Every component you build follows this pattern:

#### Phase 1: Concept (10-15 min)
- Understand the WHY before the HOW
- Ask questions until it clicks
- See examples and use cases
- Connect to previous learning

#### Phase 2: Design (5-10 min)
- Design the interface together
- Propose your approach
- Discuss tradeoffs
- Agree on the simplest starting point

#### Phase 3: Build (30-60 min)
- Write code incrementally
- Test each piece before moving on
- Ask questions as they arise
- Real-time guidance and debugging

#### Phase 4: Validate (15-20 min)
- Test against multiple scenarios
- Find and fix edge cases
- Understand failure modes
- Document what works/doesn't

#### Phase 5: Reflect (10 min)
- What did you learn?
- What surprised you?
- How does it connect to theory?
- Update your learning tracker

---

## Context Continuity System

### File Structure
```
ai-agents-course/
├── LEARNING_TRACKER.md          # Your progress and current state
├── SESSION_NOTES/               # Notes from each session
│   ├── 2025-01-30-module1-complete.md
│   ├── 2025-01-31-module2-day1.md
│   └── ...
├── modules/
│   ├── module1_agent_loop/
│   ├── module2_tools/
│   └── ...
├── exercises/                   # Retention exercises
│   ├── module1_exercise.md
│   └── ...
└── docs/
    ├── reference/               # Quick reference materials
    └── learnings/               # Key insights
```

### LEARNING_TRACKER.md Template
```markdown
# AI Agents Mastery - Learning Tracker

## Current Status
**Module:** [Current module number and name]
**Phase:** [Planning/Building/Testing/Complete]
**Last Updated:** [Date]

## Progress
- ✅ Module 1: Agent Loop
- 🔄 Module 2: Tool Use (In Progress - web_scraper complete)
- ⏳ Module 3: Memory & State
- ... [rest of modules]

## What I've Built
### Module 1: Agent Loop
- **Location:** `modules/module1_agent_loop/simple_agent.py`
- **Capabilities:** ReAct loop, web_search, calculator, currency_convertor
- **Key Learning:** Tool use API, parallel execution, stop_reason handling
- **Exercise Completed:** ✅ Built currency converter from scratch

### Module 2: Tool Use (Current)
- **Location:** `modules/module2_tools/`
- **Building:** web_scraper ✅, note_storage 🔄
- **Key Learning:** [Fill as you learn]
- **Exercise:** [Pending]

## Current Challenges
- [List any blockers or confusions]

## Insights & Aha Moments
- [Things that clicked for you]
- [Patterns you've noticed]
- [Connections between concepts]

## Tech Setup
- Python 3.11+, UV package manager
- Claude Sonnet 4 API
- GitHub: [your-repo-url]
- Tools: Tavily, BeautifulSoup, httpx

## Session Planning
**Next Session Goals:**
- [ ] [Specific task 1]
- [ ] [Specific task 2]
- [ ] [Test scenario to validate]
```

### Starting Each Session
```
Prompt: "Check my LEARNING_TRACKER.md for current state. 
Today I want to [specific goal]."
```

### Ending Each Session
1. Update LEARNING_TRACKER.md with what you built
2. Note any questions or challenges
3. Plan next session goals
4. Commit to GitHub
5. (Optional) Create session note in SESSION_NOTES/

---

## Complete Module Breakdown

### Module 1: The Agent Loop ✅
**Status:** Completed
**Duration:** 3-4 days
**Core Concept:** Understanding the Observe-Think-Act-Repeat pattern

**What You Built:**
- ReAct agent from scratch
- Tool execution system
- Basic error handling

**Retention Exercise:** Build a simple calculator agent from memory

---

### Module 2: Tool Use & Function Calling 🔄
**Status:** Current
**Duration:** 4-5 days
**Core Concept:** Building production-grade tools with proper error handling

#### Components to Build:

**2.1: Web Scraper (Day 1-2)**
- Concept: HTTP → Parse → Clean pipeline
- Build Iterations:
  1. Basic HTTP request
  2. Add BeautifulSoup parsing
  3. Remove noise (nav, footer, scripts)
  4. Add error handling
  5. Create tool schema
  6. Integrate with agent
- Test Cases:
  - Scrape example.com (success)
  - Scrape 404 page (handle error)
  - Scrape paywalled site (detect and report)

**2.2: Note Storage (Day 2-3)**
- Concept: Persistent state via JSONL
- Build Iterations:
  1. Basic save function
  2. Add metadata (timestamp, tags)
  3. Create retrieval functions
  4. Add search capability
  5. Create tool schema
  6. Integrate with agent
- Test Cases:
  - Save a note and retrieve it
  - Save multiple notes, filter by tags
  - Handle duplicate titles
  - Persist across Python restarts

**2.3: Integration (Day 4)**
- Agent with all tools working
- Test workflow: search → scrape → save
- Test parallel execution
- Debug and refine

**2.4: Validation (Day 5)**
- Complete end-to-end tests
- Document what you learned
- Update LEARNING_TRACKER

**Retention Exercise:** 
Build a "News Research Agent" from scratch that can:
- Search for news on a topic
- Scrape article content
- Save summaries with dates
- Retrieve saved articles by date/topic

**Deliverable:** Working agent + written reflection on what you learned

---

### Module 3: Memory & State Management
**Duration:** 3-4 days
**Core Concept:** Short-term, long-term, and working memory

#### Components to Build:

**3.1: Conversation Memory**
- Store conversation history
- Implement summarization
- Context window management

**3.2: Persistent Knowledge Base**
- Extend note storage from Module 2
- Add semantic search
- Implement retrieval strategies

**3.3: Working Memory**
- Track current task state
- Implement state serialization
- Add recovery mechanisms

**Retention Exercise:**
Build a "Personal Research Assistant" that:
- Remembers past conversations
- Can recall "What did we discuss about X?"
- Maintains research context across sessions
- Suggests related topics based on history

---

### Module 4: LangChain - Framework Abstraction
**Duration:** 5-6 days
**Core Concept:** Understanding what frameworks abstract away

#### Components to Build:

**4.1: Compare Raw vs Framework**
- Take your Module 2 agent
- Rewrite using LangChain
- Document differences

**4.2: LangChain Patterns**
- Chains
- Prompt templates
- Output parsers
- Callbacks

**Retention Exercise:**
Build the same "News Research Agent" using LangChain.
Compare:
- Lines of code
- Complexity
- What you gained
- What you lost

---

### Module 5: LangGraph - Multi-Agent Systems
**Duration:** 6-7 days
**Core Concept:** Stateful workflows and agent coordination

#### Components to Build:

**5.1: Graph-Based Architecture**
- State management in graphs
- Conditional edges
- Routing logic

**5.2: Multi-Agent Team**
- Researcher agent
- Analyst agent
- Writer agent
- Supervisor agent

**Retention Exercise:**
Build a "Competitive Intelligence Team" where:
- Researcher finds competitor info
- Analyst compares features/pricing
- Writer generates battle cards
- Supervisor coordinates the team

This applies directly to your capstone project.

---

### Module 6: RAG + Agents
**Duration:** 5-6 days
**Core Concept:** Knowledge-augmented intelligence

#### Components to Build:

**6.1: Vector Database**
- Document chunking
- Embeddings generation
- Similarity search

**6.2: Agentic RAG**
- Agent decides when to retrieve
- Query transformation
- Reranking strategies

**6.3: Model Context Protocol (MCP)**
- Understanding MCP
- Implementing MCP tools
- Integration patterns

**Retention Exercise:**
Build a "Documentation Assistant" that:
- Ingests competitor docs (PDFs, web pages)
- Answers questions using RAG
- Cites sources accurately
- Knows when it doesn't know

---

### Module 7: Planning & Self-Correction
**Duration:** 4-5 days
**Core Concept:** Making agents reason about their approach

#### Components to Build:

**7.1: Planning Layer**
- Plan-and-execute pattern
- Task decomposition
- Progress tracking

**7.2: Reflection & Critique**
- Self-evaluation
- Confidence scoring
- Error recovery

**Retention Exercise:**
Build a "Research Planner" that:
- Takes a complex query
- Creates a research plan
- Executes systematically
- Self-corrects when needed
- Reports confidence in findings

---

### Module 8: Evaluation & Testing
**Duration:** 4-5 days
**Core Concept:** Making agents reliable and measurable

#### Components to Build:

**8.1: Test Harness**
- Golden test cases
- Automated evaluation
- Regression testing

**8.2: Observability**
- Tracing with LangSmith
- Metrics and monitoring
- Cost tracking

**8.3: Guardrails**
- Handling hallucinations
- Safety checks
- Error boundaries

**Retention Exercise:**
Build a test suite for your competitive intelligence agent:
- 10 golden test cases
- Automated accuracy scoring
- Performance benchmarks
- Cost analysis

---

### Module 9: Production Deployment
**Duration:** 5-6 days
**Core Concept:** From prototype to production service

#### Components to Build:

**9.1: API Design**
- REST API for agent
- Authentication
- Rate limiting

**9.2: Infrastructure**
- Docker containerization
- AWS deployment
- Scaling considerations

**9.3: Production Patterns**
- Async execution
- Job queues
- Monitoring and alerts

**Retention Exercise:**
Deploy your competitive intelligence agent as:
- A REST API
- Accessible to team members
- With monitoring dashboard
- With cost controls

---

### Bonus Module: Root Cause Analysis Agent
**Duration:** 5-7 days
**Core Concept:** Applying everything to your work use case

#### Components to Build:
- Integration with observability data sources
- Pattern recognition in incident data
- Causal reasoning and hypothesis generation
- Integration with ticketing systems
- Human-in-the-loop validation

**Final Exercise:**
Build a production-ready RCA agent for your team.

---

## Retention Strategy

### After Each Module:

**1. Immediate Retention (Same Day)**
- Write a 1-page summary: "What did I learn?"
- List 3 key concepts
- Note 1 thing that surprised you

**2. Practice Exercise (Within 48 hours)**
- Build the module's retention exercise
- Do it WITHOUT looking at your code
- See what you remember vs forgot
- Review concepts you struggled with

**3. Week Review (Every 7 days)**
- Review your module summaries
- Identify patterns across modules
- Update your LEARNING_TRACKER with insights

**4. Teaching Test (Every 2 weeks)**
- Explain a concept to someone (or write it out)
- If you can't explain it simply, you don't understand it
- Revisit that concept

---

## Progress Tracking

### Weekly Reflection Template
```markdown
# Week [N] - [Date Range]

## Modules Completed
- [List modules finished this week]

## Key Learnings
1. [Concept that clicked]
2. [Pattern you noticed]
3. [Skill you developed]

## Challenges Overcome
- [Problem you solved]
- [How you solved it]

## Questions Still Open
- [Things you're still unsure about]

## Next Week Goals
- [ ] [Specific goal 1]
- [ ] [Specific goal 2]
```

### Milestone Checkpoints

**After Module 3 (Foundations Complete):**
- You should be able to build a functional agent with tools and memory
- Checkpoint exercise: Build a simple agent from scratch in 2 hours

**After Module 6 (Frameworks & Patterns):**
- You should understand when to use frameworks vs raw code
- Checkpoint exercise: Architect a new agent system on paper

**After Module 9 (Production Ready):**
- You should be able to deploy a production agent
- Final checkpoint: Complete capstone project

---

## Success Metrics

You've mastered AI agents when you can:

✅ Explain the ReAct pattern to a colleague  
✅ Build a new agent from scratch in under 4 hours  
✅ Debug tool execution issues systematically  
✅ Design tool schemas that Claude uses effectively  
✅ Choose appropriate architecture for a use case  
✅ Implement proper error handling and recovery  
✅ Deploy an agent as a production service  
✅ Evaluate and improve agent performance  
✅ Read LangChain/LangGraph code and understand it  
✅ Architect multi-agent systems confidently  

---

## Getting Started

### Day 1 Setup (30 minutes)

1. **Create file structure:**
```bash
cd ~/ai-agents-course
mkdir -p SESSION_NOTES exercises docs/reference docs/learnings
touch LEARNING_TRACKER.md
```

2. **Initialize GitHub:**
```bash
git init
git add .
git commit -m "Initial setup - Learning system"
# Create repo on GitHub, then:
git remote add origin [your-repo-url]
git push -u origin main
```

3. **Set up Project in Claude.ai:**
- Add LEARNING_TRACKER.md to Project Knowledge
- Add this curriculum document
- Add your main code files

4. **First Session:**
```
"Check my LEARNING_TRACKER.md. I'm ready to start Module 2.
Let's begin with the web_scraper component."
```

---

## Questions? Adjustments?

This curriculum is YOUR learning journey. We can:
- Adjust pace based on your schedule
- Spend more time on concepts you find challenging
- Skip concepts you already understand deeply
- Customize exercises to your interests
- Pivot focus based on your work needs

**The goal: Deep understanding, not just completion.**

---

*Last Updated: 2025-01-31*
*Next Review: After Module 2 completion*
