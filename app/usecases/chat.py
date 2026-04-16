from app.core.errors import ExternalServiceError
from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self, repo: ChatMessagesRepository, client: OpenRouterClient):
        self._repo = repo
        self._client = client

    async def ask(
        self,
        *,
        user_id: int,
        prompt: str,
        system: str | None,
        max_history: int,
        temperature: float,
    ) -> str:
        messages: list[dict] = []

        if system:
            messages.append({"role": "system", "content": system})

        if max_history > 0:
            history = await self._repo.get_last_messages(
                user_id=user_id, limit=max_history
            )
            for m in history:
                messages.append({"role": m.role, "content": m.content})

        messages.append({"role": "user", "content": prompt})

        await self._repo.add_message(user_id=user_id, role="user", content=prompt)

        try:
            answer = await self._client.chat_completions(
                messages=messages, temperature=temperature
            )
        except ExternalServiceError:
            raise
        except Exception as e:
            raise ExternalServiceError("Ошибка при обращении к OpenRouter") from e

        await self._repo.add_message(user_id=user_id, role="assistant", content=answer)
        return answer

    async def history(self, *, user_id: int, limit: int) -> list:
        return await self._repo.get_last_messages(user_id=user_id, limit=limit)

    async def clear_history(self, *, user_id: int) -> None:
        await self._repo.delete_history(user_id=user_id)
