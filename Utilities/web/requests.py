import aiohttp

async def async_get(url, headers=None):
    """Get a JSON response from a URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, raise_for_status=True) as resp:
            response = await resp.json()
            return response
        
async def async_post(url, headers=None, data=None):
    """Post to a URL asynchronously."""
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data, raise_for_status=True) as resp:
            response = await resp.json()
            return response