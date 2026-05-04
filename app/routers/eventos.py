from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
import httpx

from app.core.config import settings
from app.core.dependencies import get_current_user, extract_role

router = APIRouter(prefix="/eventos")

_HOP_BY_HOP = {"transfer-encoding", "connection"}


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_eventos(
    path: str,
    request: Request,
    user: dict = Depends(get_current_user),
):
    role = extract_role(user) if user else "anonymous"
    target_url = f"{settings.EVENTOS_SERVICE_URL}/{path}"
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"

    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() not in ("host", "content-length")
    }
    headers["X-User-Role"] = role

    body = await request.body()
    client: httpx.AsyncClient = request.app.state.http_client

    try:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            follow_redirects=False,
        )
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="Eventos service unavailable")
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Eventos service timeout")

    resp_headers = {k: v for k, v in response.headers.items() if k.lower() not in _HOP_BY_HOP}
    return Response(content=response.content, status_code=response.status_code, headers=resp_headers)
