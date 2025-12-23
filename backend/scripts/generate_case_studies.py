import asyncio
import json
import openai
from jsonschema import validate, ValidationError

from app.core.config import settings

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "Title": {"type": "string", "description": "Concise, descriptive title."},
        "Industry": {"type": "string", "description": "Industry name (e.g., Finance, Healthcare)."},
        "Technologies": {"type": "array", "items": {"type": "string"}, "description": "Array of technology tags (e.g., 'UI/UX Design', 'Cloud Computing', 'AI/ML')."},
        "SolutionsProvided": {"type": "array", "items": {"type": "string"}, "description": "List of implemented solutions (e.g., 'chatbot integration', 'data visualization')."},
        "Services": {"type": "array", "items": {"type": "string"}, "description": "List of offered services (e.g., 'Architecture Design', 'Safety Analysis', 'Hardware Design')."},
        "DetailedContent": {"type": "string", "description": "Narrative summary detailing challenges, methodologies, and outcomes."},
        "SourceURL": {"type": "string", "description": "Dummy URL simulating a SharePoint link."}
    },
    "required": ["Title", "Industry", "Technologies", "SolutionsProvided", "Services", "DetailedContent", "SourceURL"]
}

SYSTEM_PROMPT = f"""
    You are an expert synthetic data generator. Your task is to generate case study records based on the following structure and instructions.

    ---

    ### **STRICT OUTPUT FORMAT CRITICAL INSTRUCTION**

    The entire output MUST be a single JSON object. This object MUST contain only one top-level key named **'records'**. The value associated with the 'records' key MUST be a JSON array (list) containing all the generated case study records.

    **ALL FIELDS ARE REQUIRED AND MUST BE POPULATED WITH DATA.**
    All seven keys ('Title', 'Industry', 'Technologies', 'SolutionsProvided', 'Services', 'DetailedContent', 'SourceURL') **MUST** be present in every record. Array fields **MUST NOT** be empty or null; they must contain at least one meaningful string value.

    The records must strictly follow this machine-readable schema:
    {json.dumps(JSON_SCHEMA, indent=2)}

    ---

    ### **DIRTINESS AND VARIABILITY INSTRUCTIONS (CRITICAL)**

    You must intentionally introduce the following errors and inconsistencies across the generated records, focusing on the quality and content of the data, not its presence:

    1. **Ambiguous Terminology:**
    - Replace specific technologies or services with vague terms (e.g., “data stuff”, “AI platform”, “custom system”).
    2. **Typographical Errors:**
    - Add occasional typos or inconsistent capitalization, especially in 'Title' and 'DetailedContent'.
    3. **Contradictory Statements:**
    - Occasionally include contradictions (e.g., a “secure offline system” described as “hosted entirely on the cloud”).
    4. **Incomplete Sentences:**
    - Randomly truncate 'DetailedContent' to simulate incomplete narratives.
    5. **URL Noise:**
    - Slightly alter URLs (e.g., missing trailing slash, inconsistent case, small typos in domain name).
    """

USER_MESSAGE = """
    Generate exactly {num_records} case study records following the schema and containing the specified real-world dirtiness."""

async def generate_records(client: openai.OpenAI, num_records: int):
    output_path = "scripts/case_studies.json"
    user_message = USER_MESSAGE.format(num_records=num_records)
    try:
        response = client.chat.completions.create(
            model = "l2-gpt-4.1",
            messages = [
                { "role": "system", "content": SYSTEM_PROMPT },
                { "role": "user", "content": user_message }
            ],
            response_format = { 
                "type": "json_object"
            }
        )

        json_output = response.choices[0].message.content
        data = json.loads(json_output)

        if "records" not in data:
            raise KeyError("Expected key 'records' missing in response.")
        
        records = data['records']
        validate_records(records)
        with open(output_path, 'w') as f:
            json.dump(records, f, indent=2)

    except Exception as e:
        print(f"An error occurred during generating data: {e}")
        return []
    
def validate_records(records):
    for i, record in enumerate(records):
        try:
            validate(instance=record, schema=JSON_SCHEMA)
        except ValidationError as e:
            print(f"Record {i} failed validation: {e}")

def main():
    client = openai.OpenAI(
        api_key=settings.OPENAI_API_KEY,
        base_url=settings.OPENAI_BASE_URL
    )
    asyncio.run(generate_records(client=client, num_records=50))

if __name__ == "__main__":
    main()