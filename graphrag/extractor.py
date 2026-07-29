import json
import re
from llm.provider import generate_response

def extract_entities(text: str):
    prompt = f"""
Extract entities and relationships from the following text.

Return ONLY valid JSON.

Format:
{{
    "entities":[
    {{
        "name":"",
        "type":""
    }}
],

"relationships":[
    {{
    "source":"",
    "target":"",
    "relation":""
    }}
]

}}

Text:
{text}
"""
    response = generate_response(prompt)

    # Strip markdown code block fences if present
    cleaned = response.strip()
    if cleaned.startswith("```"):
        # Remove opening fence (e.g. ```json or ```)
        cleaned = re.sub(r"^```\w*\s*", "", cleaned)
        # Remove closing fence
        cleaned = re.sub(r"\s*```$", "", cleaned)
        cleaned = cleaned.strip()

    # Try to extract a JSON object from the cleaned response
    # Find the first '{' and last '}'
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1:
        cleaned = cleaned[start:end+1]

    return json.loads(cleaned)
