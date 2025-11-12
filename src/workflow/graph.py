from fastapi import Depends
from typing import List
import os
from langgraph.graph import StateGraph, END, START
import httpx

from src.workflow.state import State
from src.workflow.application.agents.technician import Technician
from src.workflow.dependencies import get_technician
from src.shared.utils.http.get_hmac_header import generate_hmac_headers


def create_graph(
    technician: Technician = Depends(get_technician),
):
    graph = StateGraph(State)

    async def technician_node(state: State):
        response = await technician.interact(state=state)

        return {"final_response": response}


    
    async def hanlde_response_node(state: State):
        hmac_headers = generate_hmac_headers(os.getenv("HMAC_SECRET"))
        main_server = os.getenv("MAIN_SERVER_ENDPOINT")
        req_body = {
            "sender": os.getenv("AGENT_ID"),
            "message_type": "ai",
            "text": state["final_response"]
        }
        
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{main_server}/messages/internal/{state['chat_id']}",
                headers=hmac_headers,
                json=req_body
            )

            if res.status_code != 201:
                print("POST response:", res)

            return state
            

    graph.add_node("technician", technician_node)
    graph.add_node("handle_response", hanlde_response_node)

    graph.add_edge(START, "technician")
    graph.add_edge("technician", "handle_response")
    graph.add_edge("handle_response", END)

    return graph.compile()
   

