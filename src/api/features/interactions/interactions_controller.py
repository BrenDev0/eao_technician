from  fastapi import Request, BackgroundTasks
import asyncio
from src.workflow.state import State

from src.api.core.models.http_responses import CommonHttpResponse

class InteractionsController: 
    async def interact(
        self,
        background_tasks: BackgroundTasks,
        req: Request,
        state: State,
        graph,
    ) -> CommonHttpResponse:
        
        background_tasks.add_task(graph.ainvoke, state)

        return CommonHttpResponse(
            detail="Request received"
        )
  