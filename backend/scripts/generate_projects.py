import asyncio
import json
import openai
from jsonschema import validate, ValidationError

from app.core.config import settings

JSON_SCHEMA = {
    "type": "object",
    "properties": {
        "Title": {"type": "string", "description": "Descriptive project name."},
        "TechStack": {"type": "array", "items": {"type": "string"}, "description": "Array of key technologies used."},
        "SolutionsImplemented": {"type": "array", "items": {"type": "string"}, "description": "Detailed list of provided solutions."},
        "ServicesOffered": {"type": "array", "items": {"type": "string"}, "description": "Array of service categories (e.g., “UI/UX Design”, “Safety Analysis”)."},
        "Summary": {"type": "string", "description": "Narrative outlining project objectives and outcomes."}
    },
    "required": ["Title", "TechStack", "SolutionsImplemented", "ServicesOffered", "Summary"]
}

SYSTEM_PROMPT = f"""
    You are an expert synthetic data generator. Your task is to generate project records based on the following structure and instructions.

    ---

    ### **STRICT OUTPUT FORMAT CRITICAL INSTRUCTION**

    The entire output MUST be a single JSON object. This object MUST contain only one top-level key named **'records'**. The value associated with the 'records' key MUST be a JSON array (list) containing all the generated project records.

    **ALL FIELDS ARE REQUIRED AND MUST BE POPULATED WITH DATA.**
    All five keys ('Title', 'TechStack', 'SolutionsImplemented', 'ServicesOffered', 'Summary') **MUST** be present in every record. Array fields **MUST NOT** be empty or null; they must contain at least one meaningful string value.

    The records must strictly follow this machine-readable schema:
    {json.dumps(JSON_SCHEMA, indent=2)}

    ---

    ### **DIRTINESS AND VARIABILITY INSTRUCTIONS (CRITICAL)**

    You must intentionally introduce the following errors and inconsistencies across the generated records, focusing on the quality and content of the data, not its presence:

    1.  **Ambiguous Terminology:**
        * Replace specific, clear terms with **vague or ambiguous terminology** (e.g., use 'SQL Database' instead of 'PostgreSQL', or 'Cloud Compute' instead of 'AWS Lambda').

    2.  **Typographical Errors:**
        * Introduce occasional **typos, misspellings, or missing punctuation** in the 'Title' and 'Summary' fields.

    3.  **Contradictory Statements:**
        * For some records, ensure the **'Summary' narrative directly contradicts** a technical detail or service category listed in 'TechStack' or 'ServicesOffered' (e.g., Summary mentions "fully proprietary solution" but TechStack lists "GPL v3 License").

    4.  **Incomplete Sentences:**
        * Randomly **truncate the 'Summary' field** to simulate incomplete entries or data cuts.
    """

USER_MESSAGE = """
    Generate exactly {num_records} project records following the schema and containing the specified real-world dirtiness."""

async def generate_records(client: openai.OpenAI, num_records: int):
    output_filename = "scripts/projects.json"
    user_message = USER_MESSAGE.format(num_records=num_records)
    try:
        response = client.chat.completions.create(
            model = settings.OPENAI_SYNTHETIC_DATA_MODEL,
            temperature = settings.OPENAI_SYNTHETIC_DATA_TEMPERATURE,
            max_tokens = settings.OPENAI_SYNTHETIC_DATA_MAX_TOKENS,
            top_p=settings.OPENAI_SYNTHETIC_DATA_TOP_P,
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
        with open(output_filename, 'w') as f:
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