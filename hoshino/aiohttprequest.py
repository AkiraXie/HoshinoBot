from typing import Any
from aiohttp import ClientResponse,ClientSession
from aiohttp.typedefs import StrOrURL


async def get(url: StrOrURL, *, allow_redirects: bool = True, **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.get(url, allow_redirects=allow_redirects, **kwargs)


async def options(url: StrOrURL, *, allow_redirects: bool = True, **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.options(url, allow_redirects=allow_redirects, **kwargs)


async def head(url: StrOrURL, *, allow_redirects: bool = False, **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.head(url, allow_redirects=allow_redirects, **kwargs)


async def post(url: StrOrURL, *, data: Any = None, **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.post(url, data=data, **kwargs)


async def put(url: StrOrURL, *, data: Any = None, **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.put(url, data=data, **kwargs)


async def patch(url: StrOrURL, *, data: Any = None, **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.patch(url, data=data, **kwargs)


async def delete(url: StrOrURL,  **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.delete(url, **kwargs)


async def request(method: str, url: StrOrURL,  **kwargs: Any) -> ClientResponse:
    async with ClientSession() as client:
        return await client.request(method, url, **kwargs)
