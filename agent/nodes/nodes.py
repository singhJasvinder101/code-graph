from langchain_core.globals import set_verbose, set_debug
from langchain_core.messages import HumanMessage
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from agent.llm import llm
from agent.tools import read_file, write_file, get_current_directory, run_cmd, init_project_root
from agent.schema import Plan, TaskPlan, CoderState
from agent.prompts import planner_prompt, architect_prompt, coder_system_prompt

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
    coder_tools = [read_file, write_file, get_current_directory, run_cmd]
    coder_state = state.get("coder_state")

    if coder_state is None:
        init_project_root()
        coder_state = CoderState(
            task_plan=state["task_plan"],
            current_step_idx=0,
        )
    
    if coder_state.current_step_idx >= len(coder_state.task_plan.implementation_steps):
        return {"coder_state": coder_state, "status": "DONE"}

    steps = coder_state.task_plan.implementation_steps
    current_step_idx = coder_state.current_step_idx

    current_step = steps[current_step_idx]

    exisiting_content = read_file.invoke({"path": current_step.filepath})
    
    coder_prompt = coder_system_prompt()
    prompt = (
        f"Task: {current_step.task_description}\n"
        f"File: {current_step.filepath}\n"
        f"Existing content:\n{exisiting_content}\n"
        "Use write_file(path, content) to save your changes."
    )

    react_agent = create_react_agent(llm, coder_tools)
    res = react_agent.invoke({
        "messages": [
            SystemMessage(content=coder_prompt),
            HumanMessage(content=prompt),
        ]
    })

    coder_state.current_step_idx += 1
    return {"coder_state": coder_state}

def normalChatAgent(state: dict) -> dict:
    prompt = state["prompt"]
    res = llm.invoke(prompt)
    return {"response": res}
    