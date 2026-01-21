import asyncio
from typing import List
from deepeval.evaluate import ErrorConfig
from deepeval.metrics import FaithfulnessMetric
from deepeval import evaluate

from app.dependencies import get_query_preprocessor, get_rag_workflow, get_weaviate_manager, get_project_repo, get_case_study_repo, get_llm_service, get_nlp_processor, get_aggregator
from evaluation.metrics.ambiguous_intent_clarification_metric import ambiguous_intent_clarification_metric
from evaluation.metrics.no_results_clarification_metric import no_results_clarification_metric
from evaluation.metrics.attribute_coverage_metric import AttributeCoverageMetric
from evaluation.metrics.intent_accuracy_metric import IntentAccuracyMetric
from evaluation.metrics.latency_metric import LatencyMetric
from evaluation.metrics.score_threshold_metric import ScoreThresholdMetric
from evaluation.utils import run_scenario_test
from evaluation.evaluation_llm import EvaluationLLM
from evaluation.golden_dataset import dataset

async def run_evaluation():
    results = []  
    custom_model = EvaluationLLM()
    faithfulness_metric = FaithfulnessMetric(
        threshold=0.7,
        model=custom_model,
        include_reason=True
    )
    score_threshold_metric = ScoreThresholdMetric(min_score=0.6)
    intent_accuracy_metric = IntentAccuracyMetric()
    latency_metric = LatencyMetric(max_seconds=40)
    project_attribute_coverage_metric = AttributeCoverageMetric(
        model=custom_model,
        target_attributes=["TECH STACK", "SOLUTIONS IMPLEMENTED", "SERVICES OFFERED"]
    )
    case_study_attribute_coverage_metric = AttributeCoverageMetric(
        model=custom_model,
        target_attributes=["INDUSTRY", "TECHNOLOGIES", "SOLUTIONS PROVIDED", "SERVICES"]
    )

    weaviate_manager = get_weaviate_manager()
    await weaviate_manager.connect()

    try:
        llm = get_llm_service()
        nlp = get_nlp_processor(llm_service=llm)
        workflow = get_rag_workflow(
            project_repo=get_project_repo(),
            case_study_repo=get_case_study_repo(),
            nlp_processor=nlp,
            llm_service=llm,
            aggregator=get_aggregator(),
            query_preprocessor=get_query_preprocessor()
        )

        test_cases = await asyncio.gather(*[run_scenario_test(workflow, g) for g in dataset])
        case_study_cases = [tc for tc in test_cases if tc.additional_metadata["scenario"] in ["case_study_sum"]]
        case_study_cases_result = evaluate(
            case_study_cases, 
            metrics=[intent_accuracy_metric, case_study_attribute_coverage_metric, faithfulness_metric, latency_metric],
            error_config=ErrorConfig(ignore_errors=True))
        results.append({"scenario": "Case study summarization", "results": case_study_cases_result})

        project_cases = [tc for tc in test_cases if tc.additional_metadata["scenario"] in ["project_match"]]
        project_cases_result = evaluate(
            project_cases, 
            metrics=[intent_accuracy_metric, project_attribute_coverage_metric, score_threshold_metric, faithfulness_metric, latency_metric],
            error_config=ErrorConfig(ignore_errors=True))
        results.append({"scenario": "Project matching", "results": project_cases_result})

        ambiguous_intent_clarification_cases = [tc for tc in test_cases if tc.additional_metadata["scenario"] in ["ambiguous_intent"]]
        ambiguous_intent_clarification_cases_result = evaluate(
            ambiguous_intent_clarification_cases, 
            metrics=[intent_accuracy_metric, ambiguous_intent_clarification_metric, latency_metric],
            error_config=ErrorConfig(ignore_errors=True))
        results.append({"scenario": "Ambiguous intent", "results": ambiguous_intent_clarification_cases_result})

        no_results_clarification_cases = [tc for tc in test_cases if tc.additional_metadata["scenario"] in ["no_results"]]
        no_results_clarification_cases_result = evaluate(
            no_results_clarification_cases, 
            metrics=[intent_accuracy_metric, no_results_clarification_metric, latency_metric],
            error_config=ErrorConfig(ignore_errors=True))
        results.append({"scenario": "No results", "results": no_results_clarification_cases_result})

        generate_report(results)

    finally:
        await weaviate_manager.disconnect()

def generate_report(results: List):
    print("\n" + "="*50)
    print("RAG EVALUATION FINAL SUMMARY")
    print("="*50)

    for res in results:
        scenario_name = res['scenario']
        evaluation_result_object = res['results']
        results_list = evaluation_result_object.test_results 
        
        total_cases = len(results_list)
        if total_cases == 0:
            print(f"\nScenario: {scenario_name} - No test cases run.")
            continue

        metric_scores = {}
        successful_cases = 0

        for test_case_result in results_list:
            if test_case_result.success:
                successful_cases += 1
            
            for metric in test_case_result.metrics_data:
                name = metric.name
                if name not in metric_scores:
                    metric_scores[name] = []
                
                metric_scores[name].append(metric.score)

        pass_rate = (successful_cases / total_cases) * 100
        print(f"\n Scenario: {scenario_name}")
        print(f" Overall Pass Rate: {pass_rate:.1f}% ({successful_cases}/{total_cases})")
        
        for metric_name, scores in metric_scores.items():
            valid_scores = [score for score in scores if score is not None]
            avg_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
            print(f"  - Avg {metric_name}: {avg_score:.4f}")
    
    print("\n" + "="*50)

def main():
    asyncio.run(run_evaluation())

if __name__ == "__main__":
    main()