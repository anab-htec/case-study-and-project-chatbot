from typing import Annotated
from fastapi import Depends

from app.repositories.interfaces.case_study_repo import CaseStudyRepository
from app.repositories.interfaces.project_repo import ProjectRepository
from app.repositories.weaviate_manager import WeaviateManager
from app.services.interfaces.llm_service import LLMService
from app.services.interfaces.nlp_processor import NLPProcessor
from app.services.query_preprocessor import QueryPreprocessor
from app.services.rag_workflow import RagWorkflow
from app.services.llm_nlp_processor import LLMNLPProcessor
from app.services.openai_llm_service import OpenAILLMService
from app.services.weighted_aggregator import WeightedAggregator
from app.services.workflow_manager import WorkflowManager

weaviate_manager = WeaviateManager()
workflow_manager = WorkflowManager()

def get_weaviate_manager() -> WeaviateManager:
    return weaviate_manager

def get_workflow_manager() -> WorkflowManager:
    return workflow_manager

def get_project_repo() -> ProjectRepository:
    return weaviate_manager.get_project_repo()

def get_case_study_repo() -> CaseStudyRepository:
    return weaviate_manager.get_case_study_repo()

def get_llm_service() -> LLMService:
    return OpenAILLMService()

def get_aggregator() -> WeightedAggregator:
    return WeightedAggregator()

def get_query_preprocessor() -> QueryPreprocessor:
    return QueryPreprocessor()

def get_nlp_processor(
        llm_service: Annotated[LLMService, Depends(get_llm_service)],
    ) -> NLPProcessor:
        return LLMNLPProcessor(llm_service=llm_service)

def get_rag_workflow(
        project_repo: Annotated[ProjectRepository, Depends(get_project_repo)],
        case_study_repo: Annotated[CaseStudyRepository, Depends(get_case_study_repo)],
        nlp_processor: Annotated[NLPProcessor, Depends(get_nlp_processor)],
        llm_service: Annotated[LLMService, Depends(get_llm_service)],
        aggregator: Annotated[WeightedAggregator, Depends(get_aggregator)],
        query_preprocessor: Annotated[QueryPreprocessor, Depends(get_query_preprocessor)]
    ) -> RagWorkflow:
        return RagWorkflow(
            project_repo=project_repo, 
            case_study_repo=case_study_repo, 
            nlp_processor=nlp_processor, 
            llm_service=llm_service,
            aggregator=aggregator,
            query_preprocessor=query_preprocessor
        )

RagWorkflowDep = Annotated[RagWorkflow, Depends(get_rag_workflow)]
WorkflowManagerDep = Annotated[WorkflowManager, Depends(get_workflow_manager)]
