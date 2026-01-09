from typing import Any
import httpx


async def http_get_text_async(url: str, headers: dict | None = None) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    

def http_get_file(url: str, dest_file_name: str, headers: Any = None, chunk_size: int = 8192, **kwargs) -> None:
    with httpx.stream("GET", url, headers=headers, **kwargs) as response:
        response.raise_for_status()
        with open(dest_file_name, "wb") as file:
            for chunk in response.iter_bytes(chunk_size):
                file.write(chunk)


def http_get(url: str, headers: Any = None) -> httpx.Response:
    with httpx.Client() as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        return response
