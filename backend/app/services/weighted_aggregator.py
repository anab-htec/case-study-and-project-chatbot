from typing import List, TypeVar, Dict, Tuple

from app.models.weighted_search_result import WeightedSearchResult

T = TypeVar("T")

class WeightedAggregator:

    def aggregate(self, weighted_search_results: List[WeightedSearchResult[T]]) -> List[Tuple[T, float]]:
        if not weighted_search_results:
            return []

        weights = [item.weight for item in weighted_search_results]
        total_weight = sum(weights)

        if (total_weight != 1.0):
            raise ValueError("The sum of all weights must be 1.")

        aggregated_results: Dict[str, Tuple[T, float]] = {}

        for weighted_search_result in weighted_search_results:
            weight = weighted_search_result.weight

            for result in weighted_search_result.results:
                id = result.id
                score = result.certainty if result.certainty is not None else 0.0
                weighted_contribution = weight * score

                if id not in aggregated_results:
                    aggregated_results[id] = (result.obj, weighted_contribution)
                else:
                    obj, existing_score = aggregated_results[id]
                    aggregated_results[id] = (obj, existing_score + weighted_contribution)

        return list(aggregated_results.values())