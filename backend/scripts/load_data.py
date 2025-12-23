
import asyncio
import json
from app.repositories.weaviate_manager import WeaviateManager
from app.dependencies import get_weaviate_manager, get_llm_service
from app.services.openai_llm_service import OpenAILLMService

async def load(manager: WeaviateManager, llm_service: OpenAILLMService):
    try:
        print("Connecting to Weaviate")
        await manager.connect()      
        print("Connection estabished")
        
        print("Loading data started")
        project_repo = manager.get_project_repo()
        case_study_repo = manager.get_case_study_repo()

        print("Creating project schema")
        await project_repo.create_schema()

        print("Creating case study schema")
        await case_study_repo.create_schema()

        print("Loading projects")
        with open('data/projects.json', "r", encoding="utf-8") as f:
            projects = json.load(f)

        for project in projects:
            technical_values = " ".join(project["TechStack"]) + " " + " ".join(project["SolutionsImplemented"])
            technical_vector = await llm_service.generate_embedding(technical_values)

            service_values = " ".join(project["ServicesOffered"])
            service_vector = await llm_service.generate_embedding(service_values)

            await project_repo.insert_project(
                properties = {
                    "title": project["Title"],
                    "techStack": project["TechStack"],
                    "solutionsImplemented": project["SolutionsImplemented"],
                    "servicesOffered": project["ServicesOffered"],
                    "summary": project["Summary"]
                },
                vector_data = {
                    "technicalVector": technical_vector,
                    "serviceVector": service_vector
                }
            )

        print("Loading case studies")

        with open('data/case_studies.json', "r", encoding="utf-8") as f:
            case_studies = json.load(f)
            
        for case_study in case_studies:
            vector = await llm_service.generate_embedding(case_study["DetailedContent"])

            await case_study_repo.insert_case_study(
                properties = {
                    "title": case_study["Title"],
                    "industry": case_study["Industry"],
                    "technologies": case_study["Technologies"],
                    "solutionsProvided": case_study["SolutionsProvided"],
                    "services": case_study["Services"],
                    "detailedContent": case_study["DetailedContent"],
                    "sourceUrl": case_study["SourceURL"]
                },
                vector = vector
            )

        print("Loading data completed")
    except Exception as e:
        print(f"Loading data failed: {e}")
        
    finally:
        await manager.disconnect()

def main():
    weaviate_manager = get_weaviate_manager() 
    llm_service = get_llm_service()
    asyncio.run(load(manager=weaviate_manager, llm_service=llm_service))

if __name__ == "__main__":
    main()