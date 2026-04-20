import pytest
import respx
from httpx import Response

from app.services.openrouter_client import OpenRouterClient
from app.core.config import settings


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_client_success():
    route = respx.post(
        f"{settings.openrouter_base_url}/chat/completions"
    ).mock(
        return_value=Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": "Тестовый ответ от модели"
                        }
                    }
                ]
            },
        )
    )

    client = OpenRouterClient()
    answer = await client.ask("Привет")

    assert route.called
    assert answer == "Тестовый ответ от модели"


@pytest.mark.asyncio
@respx.mock
async def test_openrouter_client_http_error():
    respx.post(
        f"{settings.openrouter_base_url}/chat/completions"
    ).mock(
        return_value=Response(
            401,
            json={"error": "Unauthorized"},
        )
    )

    client = OpenRouterClient()

    with pytest.raises(Exception):
        await client.ask("Привет")