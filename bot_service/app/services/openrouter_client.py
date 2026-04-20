import httpx

from app.core.config import settings


class OpenRouterClient:
    """Клиент для обращения к OpenRouter."""

    async def ask(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
            "Content-Type": "application/json",
        }

        payload = {
            "model": settings.openrouter_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{settings.openrouter_base_url}/chat/completions",
                headers=headers,
                json=payload,
            )

        response.raise_for_status()
        data = response.json()

        return data["choices"][0]["message"]["content"]