from fastapi import APIRouter, HTTPException
from llama_index.core.workflow import InputRequiredEvent, HumanResponseEvent, StopEvent, Context

from app.dependencies import RagWorkflowDep, WorkflowManagerDep
from app.core.logging_config import logger
from app.models.chat_request import ChatRequest
from app.models.chat_response import ChatResponse
from app.models.constants import WorfklowStatus

router = APIRouter()

@router.get('/hello')
async def get_message():
    logger.info("Starting message call")
    return {"message": "hello world"}

@router.post('/workflow')
async def run_worklow(workflow: RagWorkflowDep, workflow_manager: WorkflowManagerDep, request: ChatRequest):
    try:
        workflow_id = request.workflow_id
        handler = None

        if workflow_id:
            context_dict = workflow_manager.get_context(workflow_id)
            if context_dict:
                resumed_context = Context.from_dict(workflow, context_dict)
                handler = workflow.run(ctx=resumed_context)
                handler.ctx.send_event(
                    HumanResponseEvent(
                        response=request.query
                    )
            ) 

        if handler is None:
            handler = workflow.run(query=request.query)
            workflow_id = str(handler.run_id)

        async for event in handler.stream_events():
            if isinstance(event, InputRequiredEvent):
                ctx_dict = handler.ctx.to_dict()
                await handler.cancel_run() 
                workflow_manager.save_context(workflow_id=workflow_id, context_dict=ctx_dict)         
                response = ChatResponse(
                    workflow_id=workflow_id, 
                    response=event.result,
                    status=WorfklowStatus.CLARIFICATION_REQUIRED
                )

                return response
                
            elif isinstance(event, StopEvent):
                workflow_manager.delete_context(workflow_id=workflow_id)
                result = event.result or {}
                response = ChatResponse(
                    workflow_id=workflow_id, 
                    response=result.get("answer"),
                    status=WorfklowStatus.COMPLETED,
                    context=result.get("retrieved_records")
                )

                return response

        return ChatResponse(
            workflow_id=workflow_id, 
            response="An unexpected end to the workflow occurred.", 
            status=WorfklowStatus.FAILED
        )
    except Exception as e:
        logger.error(f"Workflow failed: {e}")
        raise HTTPException(
            status_code=500,
            detail="System error occurred while processing the query"
        )