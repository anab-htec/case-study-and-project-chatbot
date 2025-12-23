export type WorkflowStatus = "clarification_required" | "completed" | "error";

export interface ChatResponse {
    workflow_id: string; 
    response: string; 
    status: WorkflowStatus;
}

export class Assistant {

    delay(ms: number) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

    async chat(query: string, workflow_id: string | null) : Promise<ChatResponse> {
        const payload = {
            workflow_id: workflow_id, 
            query: query,
        };

        const response = await fetch("/api/workflow", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            throw new Error(`API returned status ${response.status}`);
        }

        return response.json() as Promise<ChatResponse>;
    }
}