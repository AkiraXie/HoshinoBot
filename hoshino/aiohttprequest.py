'''TODO:NEED TO RE-CONSTRUCT


from typing import Any
import aiohttp
from aiohttp import ClientResponse
from aiohttp.typedefs import StrOrURL


async def get(url: StrOrURL, *, allow_redirects: bool = True, **kwargs: Any) -> ClientResponse:
    return await aiohttp.request('GET', url=url, allow_redirects=allow_redirects, **kwargs)


async def options(url: StrOrURL, *, allow_redirects: bool = True, **kwargs: Any) -> ClientResponse:
    return await aiohttp.request('OPTIONS', url, allow_redirects=allow_redirects, **kwargs)


async def head(url: StrOrURL, *, allow_redirects: bool = False, **kwargs: Any) -> ClientResponse:
    return await aiohttp.request('HEAD', url, allow_redirects=allow_redirects, **kwargs)


async def post(url: StrOrURL, *, data: Any = None, **kwargs: Any) -> ClientResponse:
    return await aiohttp.request('POST', url, data=data, **kwargs)


async def put(url: StrOrURL, *, data: Any = None, **kwargs: Any) -> ClientResponse:
    return await aiohttp.request('PUT', url, data=data, **kwargs)


async def patch(url: StrOrURL, *, data: Any = None, **kwargs: Any) -> ClientResponse:
    return await aiohttp.request('PATCH', url, data=data, **kwargs)


async def delete(url: StrOrURL,  **kwargs: Any) -> ClientResponse:
    return await aiohttp.request('DELETE', url,  **kwargs)
'''