from typing import Annotated
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import END, START
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from IPython.display import Image, display


os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "langgraph-project"


llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct")


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def make_graph():
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers"""
        return a + b

    @tool
    def subtract(a: int, b: int) -> int:
        """Subtract two numbers"""
        return a - b

    tools = [add, subtract]

    tool_node = ToolNode(tools=tools)

    llm_with_tools = llm.bind_tools(tools)

    def tool_calling_llm(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    builder = StateGraph(State)

    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools=tools))

    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges("tool_calling_llm", tools_condition)
    builder.add_edge("tools", "tool_calling_llm")
    builder.add_edge("tool_calling_llm", END)

    graph = builder.compile()

    return graph


graphs = make_graph()
