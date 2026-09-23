# Agentic Banking Operations Copilot

A production-style, local-first **Agentic AI banking operations system** built with **LangChain, LangGraph, LangSmith, Ollama, FastAPI, RAG, SQLite, Chroma, Docker, and Python**.

The project demonstrates how an enterprise AI application can combine LLM reasoning with deterministic business logic, retrieval-augmented generation, tool calling, persistent workflow state, human approval, observability, evaluation, testing, and containerized deployment.

> **Project Status:** Active development. The system is being built incrementally from the infrastructure layer through RAG, tools, LangGraph orchestration, APIs, evaluation, and deployment.

---

## Project Goal

The Agentic Banking Operations Copilot is designed as an internal banking assistant capable of answering policy questions and executing controlled banking workflows.

The system will support use cases such as:

- Answering banking policy questions using RAG
- Retrieving customer account information
- Retrieving recent transactions
- Checking card status
- Identifying lost or stolen card workflows
- Blocking cards
- Requesting replacement cards
- Creating transaction disputes
- Requiring human approval for sensitive operations
- Maintaining persistent conversation and workflow state
- Resuming interrupted agent workflows
- Tracing agent execution
- Evaluating RAG, tool selection, and approval behavior

The goal is not to build a simple chatbot.

The project is designed to demonstrate the architecture of a **stateful enterprise agent system**.

---

# Architecture

```text
                         Client
                           │
                           │ HTTP
                           ▼
                  ┌─────────────────┐
                  │     FastAPI     │
                  │    REST API     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │    LangGraph    │
                  │  Orchestration  │
                  └────────┬────────┘
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
             Qwen3 LLM             Tools
             via Ollama              │
                                     │
                      ┌──────────────┼──────────────┐
                      │              │              │
                      ▼              ▼              ▼
                  Policy Tool   Account Tools   Action Tools
                      │              │              │
                      ▼              ▼              ▼
                     RAG          Services      Approval Gate
                      │              │              │
                      ▼              ▼              ▼
               Nomic Embeddings  Repositories  Human Approval
                      │              │              │
                      ▼              ▼              ▼
                    Chroma         SQLite       Tool Execution
```

Observability and evaluation surround the agent execution:

```text
                 LangGraph Execution
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
    LLM Calls       Retrieval        Tool Calls
        │               │                │
        └───────────────┼────────────────┘
                        ▼
                    LangSmith
                        │
                 Tracing / Evals
```

---

# Core Design Principle

The architecture separates **probabilistic AI reasoning** from **deterministic business controls**.

```text
LLM
 │
 │ proposes what should happen
 ▼
LangGraph
 │
 │ controls workflow
 ▼
Tools
 │
 │ expose approved capabilities
 ▼
Services
 │
 │ enforce business rules
 ▼
Repositories
 │
 │ control data access
 ▼
Database
```

The LLM does not receive unrestricted access to the database or sensitive banking operations.

For sensitive actions, deterministic application logic controls whether human approval is required.

Example:

```text
Customer:
"My debit card was stolen. Block it and send me another one."

                 ↓

              Agent

                 ↓

        Retrieve card details

                 ↓

         Retrieve bank policy

                 ↓

      Request sensitive action

                 ↓

       Deterministic routing

                 ↓

        HUMAN APPROVAL

           /           \
      APPROVE          REJECT
         │                │
         ▼                ▼
   Execute tools       Stop action
```

---

# Technology Stack

## AI and Agent Framework

- **LangChain** — model, message, tool, retrieval, and AI application abstractions
- **LangGraph** — stateful agent workflow orchestration
- **LangSmith** — agent tracing, debugging, evaluation, and experimentation

## Local Models

- **Ollama** — local model runtime
- **Qwen3 4B** — chat, reasoning, and tool-calling model
- **Nomic Embed Text** — local embedding model

No paid LLM API is required for core inference.

---

## Backend

- Python 3.14
- FastAPI
- Pydantic
- Uvicorn

---

## Retrieval-Augmented Generation

- LangChain document processing
- Local banking policy documents
- Recursive text chunking
- Nomic embeddings through Ollama
- Chroma vector database
- Semantic similarity retrieval

---

## Persistence

- SQLite — local application database
- LangGraph SQLite Checkpointer — workflow persistence
- Chroma — local vector persistence

---

## Engineering

- Repository pattern
- Service layer
- Dependency separation
- Environment-based configuration
- Structured logging
- Error handling
- Unit testing
- Integration testing
- End-to-end testing
- AI evaluation

---

## DevOps

- Docker
- Docker Compose
- GitHub Actions
- Kubernetes deployment manifests

---

# Repository Structure

```text
agentic-banking-operations-copilot/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── dependencies.py
│   │   ├── routers/
│   │   │   ├── health.py
│   │   │   ├── chat.py
│   │   │   └── approvals.py
│   │   └── schemas/
│   │       ├── chat.py
│   │       └── approvals.py
│   │
│   ├── agent/
│   │   ├── graph.py
│   │   ├── state.py
│   │   ├── routing.py
│   │   ├── prompts.py
│   │   └── nodes/
│   │       ├── assistant.py
│   │       ├── approval.py
│   │       └── rejection.py
│   │
│   ├── tools/
│   │   ├── registry.py
│   │   ├── policy_tools.py
│   │   ├── account_tools.py
│   │   ├── card_tools.py
│   │   └── dispute_tools.py
│   │
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   │
│   ├── services/
│   │   ├── account_service.py
│   │   ├── card_service.py
│   │   └── dispute_service.py
│   │
│   ├── db/
│   │   ├── session.py
│   │   ├── models.py
│   │   └── repositories/
│   │       ├── account_repository.py
│   │       ├── card_repository.py
│   │       └── dispute_repository.py
│   │
│   ├── infrastructure/
│   │   ├── llm.py
│   │   ├── checkpointer.py
│   │   └── observability.py
│   │
│   └── core/
│       ├── config.py
│       ├── logging.py
│       ├── security.py
│       └── exceptions.py
│
├── data/
│   ├── knowledge_base/
│   │   └── policies/
│   └── seed/
│
├── runtime/
│   └── chroma/
│
├── scripts/
│   ├── ingest_knowledge.py
│   ├── seed_database.py
│   └── run_evaluations.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── evals/
│   ├── datasets/
│   ├── evaluators/
│   └── run.py
│
├── alembic/
│   └── versions/
│
├── docs/
│   ├── architecture.md
│   ├── data-flow.md
│   └── interview-guide.md
│
├── deploy/
│   └── kubernetes/
│
├── .github/
│   └── workflows/
│
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── compose.yaml
├── Makefile
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# Application Layers

## API Layer

FastAPI provides the HTTP interface.

The API layer is responsible for:

- Request validation
- Response serialization
- Dependency injection
- HTTP status management
- Calling the agent/application layer

Business logic is intentionally kept outside API routes.

---

## Agent Layer

LangGraph controls the agent workflow.

Responsibilities include:

- Maintaining agent state
- Routing between nodes
- Calling the LLM
- Executing tools
- Determining workflow transitions
- Pausing for human approval
- Resuming interrupted workflows
- Maintaining thread-level persistence

---

## Tool Layer

LangChain tools expose controlled capabilities to the AI agent.

Planned tools include:

```text
search_policy

get_account_summary

get_recent_transactions

get_card_status

block_card

request_replacement_card

create_dispute
```

Tools provide the boundary between LLM reasoning and application functionality.

---

## Service Layer

Services contain deterministic banking business logic.

Examples:

```text
AccountService
CardService
DisputeService
```

The LLM does not implement banking business rules.

---

## Repository Layer

Repositories isolate database operations from business logic.

```text
Agent
  ↓
Tool
  ↓
Service
  ↓
Repository
  ↓
Database
```

This allows the storage technology to change without redesigning the agent.

---

# RAG Pipeline

Banking policies are externalized from the LLM and retrieved when required.

```text
Policy Documents
       │
       ▼
Document Loading
       │
       ▼
Text Chunking
       │
       ▼
Nomic Embeddings
       │
       ▼
Chroma Vector Store
```

During inference:

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
Semantic Search
      │
      ▼
Relevant Policy Chunks
      │
      ▼
LLM Context
      │
      ▼
Grounded Response
```

This allows policies to evolve independently of the underlying language model.

---

# Human-in-the-Loop

Sensitive operations are not automatically executed solely because the LLM requested them.

Examples:

```text
block_card
request_replacement_card
create_dispute
```

can be routed through an approval workflow.

```text
Tool Request
     │
     ▼
Sensitive?
   /     \
 NO      YES
 │        │
 ▼        ▼
Run    Interrupt
          │
          ▼
     Human Review
       /      \
   Approve    Reject
      │          │
      ▼          ▼
   Execute      Stop
```

LangGraph checkpointing enables the workflow to pause and resume while preserving state.

---

# Agent State

The graph will maintain structured workflow state such as:

```text
messages

customer_id

request_id

pending_action

approval_status

retrieved_sources
```

Conversation messages use LangChain message types including:

- `HumanMessage`
- `AIMessage`
- `ToolMessage`
- `SystemMessage`

---

# Observability

LangSmith will be integrated for development-time observability and evaluation.

Planned observability includes:

- LLM calls
- Prompt inputs
- Agent execution
- Tool selection
- Tool arguments
- Tool responses
- Retrieval activity
- Latency
- Errors
- Evaluation runs

Core application execution will remain independent of LangSmith availability.

---

# Testing Strategy

Traditional software tests and AI evaluations are treated separately.

## Unit Tests

Validate deterministic components such as:

- Services
- Repositories
- Routing
- Security rules
- Tool behavior

## Integration Tests

Validate interaction between components such as:

- RAG retrieval
- Database operations
- Agent and tools
- LangGraph persistence

## End-to-End Tests

Validate:

```text
HTTP Request
   ↓
FastAPI
   ↓
Agent
   ↓
Tools / RAG
   ↓
Response
```

---

# AI Evaluation

AI behavior requires evaluation beyond traditional assertions.

Evaluation areas include:

### RAG Groundedness

Does the generated answer remain supported by retrieved policy information?

### Retrieval Quality

Did the system retrieve the correct policy?

### Tool Selection

Did the agent choose the correct tool for the user request?

### Tool Arguments

Did the model provide valid tool parameters?

### Approval Compliance

Did sensitive operations correctly require approval?

### Safety

Did the agent avoid exposing restricted information or bypassing controls?

---

# Local-First Development

The project is intentionally designed so the core AI workload can run locally.

```text
Qwen3 4B
    ↓
Ollama

Nomic Embed Text
    ↓
Ollama

Vector Database
    ↓
Chroma

Application Database
    ↓
SQLite

Backend
    ↓
FastAPI
```

This allows the project to be built and tested without requiring paid inference infrastructure.

---

# Docker Architecture

The application will be containerized independently from the local Ollama inference runtime.

```text
┌────────────────────────────────┐
│      Application Container     │
│                                │
│ FastAPI                        │
│ LangChain                      │
│ LangGraph                      │
│ Banking application            │
└───────────────┬────────────────┘
                │
                │ HTTP
                ▼
        ┌───────────────┐
        │    Ollama     │
        │               │
        │ qwen3:4b      │
        │ nomic-embed   │
        └───────────────┘
```

This keeps application and inference lifecycles separate.

---

# Deployment Evolution

The project is being built through the following progression:

```text
Python Application
        ↓
Local FastAPI
        ↓
Docker Image
        ↓
Docker Compose
        ↓
CI Pipeline
        ↓
Kubernetes Deployment
```

The same application architecture can later be adapted to managed infrastructure.

---

# Development Roadmap

- [x] Create local Python development environment
- [x] Connect LangChain to local Ollama
- [x] Validate Qwen3 inference through `ChatOllama`
- [ ] Application configuration
- [ ] Structured logging
- [ ] SQLite database models
- [ ] Database seed pipeline
- [ ] Repository layer
- [ ] Service layer
- [ ] Ollama infrastructure abstraction
- [ ] RAG ingestion pipeline
- [ ] Local embeddings
- [ ] Chroma vector persistence
- [ ] Semantic retrieval
- [ ] LangChain banking tools
- [ ] Tool registry
- [ ] LangGraph state
- [ ] Agent nodes
- [ ] Conditional routing
- [ ] Human-in-the-loop approval
- [ ] LangGraph checkpoint persistence
- [ ] FastAPI endpoints
- [ ] LangSmith tracing
- [ ] AI evaluation datasets
- [ ] Automated evaluators
- [ ] Unit tests
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Docker image
- [ ] Docker Compose
- [ ] GitHub Actions CI
- [ ] Kubernetes manifests
- [ ] Architecture documentation
- [ ] Interview documentation

---

# Current Development Environment

```text
Python: 3.14.4

Local LLM:
qwen3:4b

Local Embedding Model:
nomic-embed-text

Alternative Local Model:
gemma3:4b

Model Runtime:
Ollama
```

---

# Key Architectural Principles

1. **LLMs reason; deterministic code controls.**
2. **Sensitive actions require explicit authorization.**
3. **The LLM never directly accesses the database.**
4. **Tools expose narrowly defined capabilities.**
5. **Business logic lives in services, not prompts.**
6. **Repositories isolate persistence technology.**
7. **Enterprise knowledge lives outside the model and is retrieved through RAG.**
8. **Agent execution is stateful and observable.**
9. **Traditional testing and AI evaluation are separate concerns.**
10. **Inference infrastructure and application infrastructure remain decoupled.**

---

# Disclaimer

This project uses synthetic banking data and fictional banking policies for Learning.

It does not connect to real banking systems, process real financial transactions, or contain real customer information.

---

# License

This project is intended for Learning.