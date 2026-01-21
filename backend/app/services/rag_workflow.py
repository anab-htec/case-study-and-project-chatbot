import asyncio
import json
from typing import List
from llama_index.core.workflow import StartEvent, StopEvent, Workflow, step, Context, Event, InputRequiredEvent, HumanResponseEvent

from app.core.config import settings
from app.core.logging_config import logger
from app.core.prompts import PROJECT_SUMMARIZATION_SYSTEM_PROMPT, PROJECT_SUMMARIZATION_USER_MESSAGE, CASE_STUDY_SUMMARIZATION_SYSTEM_PROMPT, CASE_STUDY_SUMMARIZATION_USER_MESSAGE
from app.models.constants import Intent, FailureReason
from app.models.intent_context import IntentContext
from app.models.project import Project
from app.models.case_study import CaseStudy
from app.models.record import Record
from app.models.scored_record import ScoredRecord
from app.models.vector_search_result import VectorSearchResult
from app.models.weighted_search_result import WeightedSearchResult
from app.repositories.interfaces.case_study_repo import CaseStudyRepository
from app.repositories.interfaces.project_repo import ProjectRepository
from app.services.interfaces.llm_service import LLMService
from app.services.interfaces.nlp_processor import NLPProcessor
from app.services.query_preprocessor import QueryPreprocessor
from app.services.weighted_aggregator import WeightedAggregator

class QueryEvent(Event):
    query: str

class IntentEvent(Event):
    query: str
    intent_context: IntentContext

class ProjectRetrievalResultEvent(Event):
    query: str
    intent_context: IntentContext
    result: List[ScoredRecord[Project]]

class CaseStudyRetrievalResultEvent(Event):
    query: str
    intent_context: IntentContext
    result: List[ScoredRecord[CaseStudy]]

class FailureEvent(Event):
    intext_context: IntentContext
    reason: str

class FeedbackEvent(Event):
    feedback: str

class RagWorkflow(Workflow):

    def __init__(
            self, 
            project_repo: ProjectRepository, 
            case_study_repo: CaseStudyRepository, 
            nlp_processor: NLPProcessor, 
            llm_service: LLMService, 
            aggregator: WeightedAggregator, 
            query_preprocessor: QueryPreprocessor):
        super().__init__()
        self._project_repo = project_repo
        self._case_study_repo = case_study_repo
        self._nlp_processor = nlp_processor 
        self._llm_service = llm_service
        self._aggregator = aggregator
        self._query_preprocessor = query_preprocessor
        self._clarification_max_attempts = settings.CLARIFICATION_MAX_ATTEMPTS
        self._retrieval_top_k_case_studies = settings.RETRIEVAL_TOP_K_CASE_STUDIES
        self._retrieval_top_k_projects = settings.RETRIEVAL_TOP_K_PROJECTS

    @step
    async def start(self, ctx: Context, ev: StartEvent) -> QueryEvent:
        logger.info(f"Workflow started with query: '{ev.query}'")
        preprocessed_query = self._query_preprocessor.preprocess(ev.query)
        await ctx.store.set("state", {"chat_history": [f"User: {preprocessed_query}"], "iterations": 0})
        
        return QueryEvent(query=ev.query)
    
    @step
    async def intent_detection(self, ctx: Context, ev: QueryEvent | FeedbackEvent) -> IntentEvent | FailureEvent:
        if isinstance(ev, FeedbackEvent):
            state = await ctx.store.get('state')
            query = await self._nlp_processor.condense_query(state["chat_history"])
        else:        
            query = ev.query

        logger.info(f"Detecting intent for query: '{query}'")
        intent_context = await self._nlp_processor.process_query(query=query)
        logger.info(f"Intent detection and entity extraction completed: {intent_context.model_dump()}")
        
        if (intent_context.intent == Intent.PROJECT_MATCHING or intent_context.intent == Intent.CASE_STUDY_RETRIEVAL):
            return IntentEvent(query=query, intent_context=intent_context)
        else:
            return FailureEvent(
                intext_context=intent_context,
                reason=FailureReason.AMBIGUOUS_INTENT)
        
    @step
    async def retrieval(self, ctx: Context, ev: IntentEvent) -> ProjectRetrievalResultEvent | CaseStudyRetrievalResultEvent | FailureEvent:
        if ev.intent_context.intent == Intent.CASE_STUDY_RETRIEVAL:
            logger.info(f"Retrieval of case studies started")
            records = await self._retrieve_relevant_case_studies(ev.query)
            logger.info(f"Retrieved {len(records)} case studies.")

            if not records:
                return FailureEvent(
                    intext_context=ev.intent_context,
                    reason=FailureReason.NO_MATCHING_RECORDS)  

            return CaseStudyRetrievalResultEvent(
                query=ev.query, 
                intent_context=ev.intent_context,
                result=records)
            
        elif ev.intent_context.intent == Intent.PROJECT_MATCHING:
            logger.info(f"Retrieval of projects started")
            records = await self._retrieve_relevant_projects(
                ev.intent_context.technologies,
                ev.intent_context.solutions,
                ev.intent_context.services
            )
            logger.info(f"Retrieved {len(records)} projects.")

            if not records:
                return FailureEvent(
                    intext_context=ev.intent_context,
                    reason=FailureReason.NO_MATCHING_RECORDS)  

            return ProjectRetrievalResultEvent(
                query=ev.query, 
                intent_context=ev.intent_context,
                result=records)
        
    @step
    async def summarize_projects(self, ctx: Context, ev: ProjectRetrievalResultEvent) -> StopEvent:
        logger.info(f"Summarizing projects started")
        raw_projects = [item.record for item in ev.result]
        summary = await self._generate_summary(
            ev.query, 
            PROJECT_SUMMARIZATION_SYSTEM_PROMPT, 
            PROJECT_SUMMARIZATION_USER_MESSAGE, 
            raw_projects)

        return StopEvent(
            result={
                "answer": summary,
                "intent_context": ev.intent_context,
                "retrieved_records": ev.result
            }
        )

    @step
    async def summarize_case_studies(self, ctx: Context, ev: CaseStudyRetrievalResultEvent) -> StopEvent:
        logger.info(f"Summarizing case studies started")
        raw_case_studies = [item.record for item in ev.result]
        summary = await self._generate_summary(
            ev.query, 
            CASE_STUDY_SUMMARIZATION_SYSTEM_PROMPT, 
            CASE_STUDY_SUMMARIZATION_USER_MESSAGE, 
            raw_case_studies)
        
        return StopEvent(
            result={
                "answer": summary,
                "intent_context": ev.intent_context,
                "retrieved_records": ev.result
            }
        )
            
    @step
    async def clarification(self, ctx: Context, ev: FailureEvent) -> InputRequiredEvent | StopEvent:
        logger.warning(f"Workflow entering clarification mode. Reason: {ev.reason}")
        state = await ctx.store.get("state")
        if state["iterations"] >= self._clarification_max_attempts:
            await ctx.store.set("state", state)
            return StopEvent(
                result={
                    "answer": "Could not find an answer after multiple attempts. Please try a new query."
                }
        )

        prompt = "I'm sorry, I'm having a bit of trouble processing that. Could you please provide more details?"

        if ev.reason == FailureReason.AMBIGUOUS_INTENT:
            prompt = (
                "I’m not quite sure if you’re looking to **explore our past case studies** "
                "or if you want to **match specific project requirements** against our expertise. "
                "Could you clarify which one you're interested in?"
            )
        elif ev.reason == FailureReason.NO_MATCHING_RECORDS:
            prompt = (
                "I couldn't find any records that match those specific criteria. "
                "Could you please provide more details?"
            )
            
        state["chat_history"].append(f"Assistant: {prompt}")
        await ctx.store.set("state", state)
            
        return InputRequiredEvent(
            result=prompt,
            metadata={
                "reason": ev.reason,
                "intent_context": ev.intext_context
            }
        )
    
    @step
    async def get_feedback(self, ctx: Context, ev: HumanResponseEvent) -> FeedbackEvent:
        preprocessed_query = self._query_preprocessor.preprocess(ev.response)
        state = await ctx.store.get("state")
        state["chat_history"].append(f"User: {preprocessed_query}")
        state["iterations"] += 1      
        await ctx.store.set("state", state)

        return FeedbackEvent(feedback=preprocessed_query)
    
    async def _retrieve_relevant_case_studies(self, query: str) -> List[VectorSearchResult[CaseStudy]]:
        if not query:
            return []
        
        vector = await self._llm_service.generate_embedding(query)
        case_study_search_results = await self._case_study_repo.retrieve_case_study_records(vector, self._retrieval_top_k_case_studies)

        scored_case_studies = [
            ScoredRecord(record=item.obj, score=item.certainty) 
            for item in case_study_search_results
        ]

        if len(scored_case_studies) == 0:
            logger.warning(f"Retrieval yeilded total 0 case studies from database for tech query: {query}")
            return []
        
        relevant_case_studies = []

        if settings.CASE_STUDY_SCORE_THRESHOLD:
            relevant_case_studies = [item for item in scored_case_studies if item.score > settings.CASE_STUDY_SCORE_THRESHOLD]
            if len(relevant_case_studies) == 0:
                logger.warning(f"No case studies where found with score above threshold {settings.CASE_STUDY_SCORE_THRESHOLD} for query: {query}")
        else:
            relevant_case_studies = scored_case_studies

        return relevant_case_studies

    async def _retrieve_relevant_projects(self, technologies: List[str], solutions: List[str], services: List[str]) -> List[ScoredRecord[Project]]:
        tech_query = " ".join((technologies or []) + (solutions or []))
        tech_task = self._retrieve_projects_by_tech_stack(query=tech_query)

        service_query = " ".join(services or [])
        service_task = self._retrieve_projects_by_services(query=service_query)

        tech_records, service_records = await asyncio.gather(tech_task, service_task)
        
        aggregated_results = self._aggregator.aggregate(
            [
                WeightedSearchResult(results=tech_records, weight=settings.PROJECT_TECH_WEIGHT), 
                WeightedSearchResult(results=service_records, weight=settings.PROJECT_SERVICE_WEIGHT)
            ]
        )

        scored_projects = [
            ScoredRecord(record=project, score=score) 
            for project, score in aggregated_results 
        ]

        if len(scored_projects) == 0:
            logger.warning(f"Retrieval yeilded total 0 projects from database for tech criteria: '{tech_query}' and service criteria: '{service_query}'")
            return []
        
        relevant_projects = []

        if settings.PROJECT_SCORE_THRESHOLD:
            relevant_projects = [item for item in scored_projects if item.score > settings.PROJECT_SCORE_THRESHOLD]
            if len(relevant_projects) == 0:
                logger.warning(f"No projects where found with score above threshold {settings.PROJECT_SCORE_THRESHOLD} for tech criteria: {tech_query} and service criteria: '{service_query}'")
        else:
            relevant_projects = scored_projects

        return relevant_projects

    async def _retrieve_projects_by_tech_stack(self, query: str) -> List[VectorSearchResult[Project]]:
        if not query:
            return []
        
        vector = await self._llm_service.generate_embedding(query)
        return await self._project_repo.retrieve_project_records_by_technical_vector(vector, self._retrieval_top_k_projects)

    async def _retrieve_projects_by_services(self, query: str) -> List[VectorSearchResult[Project]]:
        if not query:
            return []
        
        vector = await self._llm_service.generate_embedding(query)
        return await self._project_repo.retrieve_project_records_by_service_vector(vector, self._retrieval_top_k_projects)
    
    async def _generate_summary(self, query: str, system_prompt: str, user_prompt: str, records: List[Record]) -> str:
        items = [record.model_dump() for record in records]
        json_data = json.dumps(items, indent=2)
        system_prompt = system_prompt.format(query=query)
        user_message = user_prompt.format(query=query, json_data=json_data)

        return await self._llm_service.generate_text(
            system_prompt=system_prompt,
            user_message=user_message
        )
    
        