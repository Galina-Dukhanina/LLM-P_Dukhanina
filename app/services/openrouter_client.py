import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    async def chat_completions(
        self, *, messages: list[dict], temperature: float
    ) -> str:
        url = f"{settings.openrouter_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "HTTP-Referer": settings.openrouter_site_url,
            "X-Title": settings.openrouter_app_name,
        }
        payload = {
            "model": settings.openrouter_model,
            "messages": messages,
            "temperature": temperature,
        }

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(url, headers=headers, json=payload)

        if resp.status_code >= 400:
            raise ExternalServiceError(
                f"OpenRouter error {resp.status_code}: {resp.text}"
            )

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            raise ExternalServiceError("Некорректный ответ OpenRouter") from e
