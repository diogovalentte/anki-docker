import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
import httpx

app = FastAPI()

BACKEND_URL = "http://localhost:8765"
VALID_API_KEY = os.getenv("ANKICONNECT_API_KEY")
if not VALID_API_KEY:
    raise ValueError("ANKICONNECT_API_KEY environment variable is not set")


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy(request: Request, full_path: str):
    try:
        json_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or missing JSON body")

    if json_data.get("key") != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API key")

    del json_data["key"]

    async with httpx.AsyncClient() as client:
        proxy_request = client.build_request(
            method=request.method,
            url=f"{BACKEND_URL}/{full_path}",
            headers={
                k: v
                for k, v in request.headers.items()
                if k.lower() not in ["host", "content-length"]
            },
            json=json_data,
        )
        response = await client.send(proxy_request, stream=True)

        return Response(
            content=await response.aread(),
            status_code=response.status_code,
            headers=dict(response.headers),
        )
