import time
from deepeval.dataset import Golden
from deepeval.test_case import LLMTestCase
from llama_index.core.workflow import StopEvent, InputRequiredEvent

from app.models.constants import Intent
from app.models.case_study import CaseStudy
from app.models.project import Project

async def run_scenario_test(workflow, golden: Golden):
    actual_output = ""    
    retrieval_context = []
    scores = []
    intent_context = None
    start_time = time.perf_counter()
    
    handler = workflow.run(query=golden.input)

    async for event in handler.stream_events():
        if isinstance(event, InputRequiredEvent):
            actual_output = event.result 
            intent_context = event.metadata.get("intent_context")
            await handler.cancel_run()

            break
            
        elif isinstance(event, StopEvent):
            result_data = event.result
            if result_data is None:
                actual_output = "Error: Workflow stopped without returning a result."
                records = []
                intent_context = None
            else:
                actual_output = result_data.get("answer", "")
                records = result_data.get("retrieved_records", [])
                intent_context = result_data.get("intent_context")
            
            if records and intent_context:
                scores = [r.score for r in records]
                
                if intent_context.intent == Intent.PROJECT_MATCHING:
                    retrieval_context = [format_project_for_eval(r.record) for r in records]
                elif intent_context.intent == Intent.CASE_STUDY_RETRIEVAL:
                    retrieval_context = [format_case_study_for_eval(r.record) for r in records]
        
            break

    latency = time.perf_counter() - start_time

    return LLMTestCase(
        input=golden.input,
        actual_output=actual_output,
        expected_output=golden.expected_output or "No specific expected output required.",
        retrieval_context=retrieval_context,
        additional_metadata={
            **golden.additional_metadata,
            "latency": latency,
            "similarity_scores": scores,
            "actual_intent": intent_context.intent if intent_context else None
        }
    )

def format_case_study_for_eval(case_study: CaseStudy) -> str:
    """
    Converts a CaseStudy model into a structured string for DeepEval's 
    retrieval_context, ensuring Industry, Tech, and Solutions are labeled.
    """
    return f""" 
    TITLE: {case_study.title}
    INDUSTRY: {case_study.industry}
    TECHNOLOGIES: {", ".join(case_study.technologies)}
    SOLUTIONS: {", ".join(case_study.solutionsProvided)}
    SERVICES: {", ".join(case_study.services)}
    DETAILED CONTENT: {case_study.detailedContent}
    SOURCE URL: {case_study.sourceUrl}
    """

def format_project_for_eval(project: Project) -> str:
    """
    Converts a Project model into a structured string for DeepEval's 
    retrieval_context, ensuring Industry, Tech, and Solutions are labeled.
    """
    return f""" 
    TITLE: {project.title}
    TECH STACK: {project.techStack}
    SOLUTIONS IMPLEMENTED: {", ".join(project.solutionsImplemented)}
    SERVICES OFFERED: {", ".join(project.servicesOffered)}
    SUMMARY: {project.summary}
    """