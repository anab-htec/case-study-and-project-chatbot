from typing import Any, Dict, Optional

ContextDict = Dict[str, Any]

class WorkflowManager:
    workflow_data: Dict[str, ContextDict] = {}

    def save_context(self, workflow_id: str, context_dict: ContextDict) -> None:
        self.workflow_data[workflow_id] = context_dict

    def get_context(self, workflow_id: str) -> Optional[ContextDict]:
        return self.workflow_data.pop(workflow_id, None)

    def delete_context(self, workflow_id: str) -> None:
        if workflow_id in self.workflow_data:
            del self.workflow_data[workflow_id]