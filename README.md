# code-graph

A LangGraph pipeline that turns a plain-language app idea into a project plan, a step-by-step implementation breakdown, and structured coder output. It uses OpenAI with Pydantic schemas so each stage returns typed JSON instead of free-form text.

## What it does

You pass in a prompt (for example, “build a todo app with auth and a REST API”). The graph runs three nodes in order:

1. **Planner** — Produces a `Plan`: app name, description, tech stack, features, and a list of files to create.
2. **Architect** — Takes that plan and returns a `TaskPlan`: ordered implementation steps, each tied to a file path and a detailed task description.
3. **Coder** — Consumes the task plan and returns a `CoderState` (structured fields for tracking progress and file content). The coder prompt assumes file tools; see below.

Output is printed from `agent/graph.py` when you run the module directly. Nothing is deployed or served as an API yet.

## Layout

```
agent/
  graph.py          # LangGraph definition and agents
  schema/schema.py  # Plan, TaskPlan, CoderState models
  prompts/prompt.py # Prompt templates per agent
  tools/tools.py    # Sandboxed read/write/list/run under generated_project/
main.py             # Stub entrypoint
```

Generated code is meant to land under `generated_project/` (created by `init_project_root()` in the tools module). Path helpers block writes outside that directory.

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (or install deps from `pyproject.toml` yourself)
- OpenAI API key in a `.env` file:

```
OPENAI_API_KEY=sk-...
```

The graph uses `gpt-4o-mini` via `langchain-openai`. Models and prompts are easy to change in `agent/graph.py`.

## Setup

```bash
git clone <repo-url>
cd code_graph
uv sync
cp .env.example .env   # if you add an example; otherwise create .env with OPENAI_API_KEY
```

## Run

```bash
uv run python -m agent.graph
```

Edit the sample prompt at the bottom of `agent/graph.py` to try something else.

Pydantic models use `extra="forbid"` because OpenAI’s strict JSON-schema mode rejects schemas that allow arbitrary extra fields. If you change the schemas, keep that in mind or switch to `method="function_calling"` on `with_structured_output`.

## Tools

`agent/tools/tools.py` defines LangChain `@tool` functions: `read_file`, `write_file`, `list_files`, `get_current_directory`, and `run_cmd`. They are scoped to `generated_project/` under the current working directory. Hooking tools up would mean binding them to the model and looping on tool results (typical agent executor pattern).

## Status

Early experiment. Planner and architect paths work end-to-end with structured output. Coder output is structured but not written to disk automatically. `main.py` is unused.
