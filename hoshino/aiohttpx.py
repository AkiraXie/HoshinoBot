import httpx
from httpx import Response


async def get(url: str, *args, **kwargs) -> Response:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, *args, **kwargs)
        return resp


async def post(url: str, *args, **kwargs) -> Response:
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, *args, **kwargs)
        return resp


async def head(url: str, *args, **kwargs) -> Response:
    async with httpx.AsyncClient() as client:
        resp = await client.head(url, *args, **kwargs)
        return resp
