from agent.schema import Plan, TaskPlan, CoderState
from agent.prompts import planner_prompt, architect_prompt, coder_system_prompt
from dotenv import load_dotenv
from langgraph.constants import END
from langgraph.constants import START
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

def plannerAgent(state: dict) -> dict:
    prompt = planner_prompt(state["prompt"])
    #print(prompt)
    res = llm.with_structured_output(Plan, method="json_schema").invoke(prompt)
    return {"plan": res}
    #pass


def architectAgent(state: dict) -> dict:
    prompt = architect_prompt(state["plan"].model_dump_json(indent=2))
    res = llm.with_structured_output(TaskPlan, method="json_schema").invoke(prompt)
    return {"task_plan": res}


def coderAgent(state: dict) -> dict:
    prompt = coder_system_prompt() + "\n\n" + state["task_plan"].model_dump_json(indent=2)
    
    res = llm.with_structured_output(CoderState, method="json_schema").invoke(prompt)
    return {"code": res}

graph = StateGraph(dict)

graph.add_node("planner", plannerAgent)
graph.add_node("architect", architectAgent)
graph.add_node("coder", coderAgent)

graph.add_edge(START, "planner")
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_edge("coder", END)

agent = graph.compile()

if __name__ == "__main__":
    result = agent.invoke(
        {"prompt": "Build a simple todo app with user authentication and a REST API."},
        {"recursion_limit": 100}
    )
    print(result)