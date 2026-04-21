import json

def build_extraction_prompt(chunk: str) -> str:
    return f"""
You are a medical information extraction system.

Extract structured data from the clinical document.

RULES:
- Output ONLY valid JSON
- No explanations
- No comments
- Missing fields → null
- Do not invent information
- Return ONLY valid JSON. No text before or after.

JSON schema:
{{
  "patient": {{
    "age": int or null,
    "sex": "male" | "female" | null
  }},
  "diagnosis": string or null,
  "findings": [string],
  "treatment": string or null
}}

The "patient" field MUST always be an object with the following structure:
{{
  "age": int or null,
  "sex": "male" | "female" | null
}}

Do NOT return "patient": null.
If unknown, return:
"patient": {{ "age": null, "sex": null }}

Document:
{chunk}

Return JSON:
"""

def build_repair_prompt(text: str, previous_json: dict, errors: str) -> str:
    return f"""
You are a clinical data extraction system correcting JSON output.

Your task is to fix a JSON object so that it strictly follows the required schema.

IMPORTANT RULES:
- Fix ONLY the fields that are invalid
- Keep all valid fields unchanged
- Do NOT remove existing correct data
- Do NOT add explanations
- Output ONLY valid JSON

SCHEMA REQUIREMENTS:
- "patient" MUST be an object with:
    - "age": integer or null
    - "sex": "male", "female", or null
- "diagnosis": string or null
- "findings": list of strings
- "treatment": string or null

VALIDATION ERRORS:
{errors}

ORIGINAL TEXT:
{text}

CURRENT JSON:
{previous_json}

Return corrected JSON only:
"""