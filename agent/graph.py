from agent import checkpointer
from dotenv import load_dotenv
from langgraph.constants import END
from langgraph.constants import START
from langgraph.graph import StateGraph
from agent.configs.checkpointer_config import *
from agent.nodes.nodes import plannerAgent, architectAgent, coderAgent, normalChatAgent

#set_debug(True)
#set_verbose(True)

graph = StateGraph(dict)

graph.add_node("planner", plannerAgent)
graph.add_node("architect", architectAgent)
graph.add_node("coder", coderAgent)
graph.add_node("normal_chat", normalChatAgent)

graph.add_edge(START, "planner")
graph.add_edge("planner", "architect")
graph.add_edge("architect", "coder")
graph.add_conditional_edges(
    "coder",
    lambda s: END if s.get("status") == "DONE" else "coder",
    {"coder": "coder", END: END},
)

agent = checkpointer.compile_with_mongo_checkpointer(graph)

if __name__ == "__main__":
    #result = agent.invoke(
    #    {"prompt": "Build a simple todo app in next.js with user authentication and a REST API."},
    #    write_config
    #)
    while True:
        query = input("Enter your query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        #result = agent.invoke({"prompt": query}, write_config)

        for chunk in agent.stream({"prompt": query}, write_config, stream_mode="values"):
            print(chunk)
        
        #print(result)