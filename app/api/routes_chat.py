from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError
from app.schemas.chat import ChatRequest, ChatResponse
from app.usecases.chat import ChatUseCase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    data: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCase = Depends(get_chat_usecase),
):
    try:
        answer = await uc.ask(
            user_id=user_id,
            prompt=data.prompt,
            system=data.system,
            max_history=data.max_history,
            temperature=data.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))


@router.get("/history")
async def history(
    limit: int = 50,
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCase = Depends(get_chat_usecase),
):
    items = await uc.history(user_id=user_id, limit=limit)
    return {
        "items": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in items
        ]
    }


@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    uc: ChatUseCase = Depends(get_chat_usecase),
):
    await uc.clear_history(user_id=user_id)
    return None
