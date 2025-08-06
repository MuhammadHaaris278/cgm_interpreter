from app.services.llm.client import get_openai_client
from app.services.llm.prompt import build_prompt

def generate_interpretation(summary: dict, recommendations: list[str]) -> str:
    """
    Sends the structured CGM summary + recommendations to GPT-4.1
    and returns the human-readable interpretation.
    """
    prompt = build_prompt(summary, recommendations)

    client = get_openai_client()
    response = client.chat.completions.create(
        model="openai/gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
