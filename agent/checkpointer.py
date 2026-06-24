from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph
from langgraph.checkpoint.mongodb import MongoDBSaver
from agent.configs.checkpointer_config import *

def compile_with_mongo_checkpointer(graph: StateGraph) -> CompiledStateGraph:
    agent = None
    with MongoDBSaver.from_conn_string(MONGODB_URI, DB_NAME) as checkpointer:
        agent = graph.compile()
    return agent