import aiohttp
import re

async def get_emoji(query: str, url: str, min_prob: int = 0.05, results: int = 5) -> list:
    """
    Get the top emoji for qiven string using a Deepmoji API instance
    
    Args
        query (str): The string you would like to send to the API.
        url (str): Link to an instance of https://github.com/nolis-llc/DeepMoji-docker.
        min_prob (int): Filter results by probability (ex. if min_prob is 0.05, no results with a probability below 0.05 will be returned)
        results (int): The maximum number of results to return.
    Returns:
        A list of dictionaries with keys "emoji" and "prob" from the API
    Raises:
        HTTPError: if the API cannot be reached or returns an invalid response.
    """
    if query:
        x = re.sub("[<>:'\"\?]|\d{5,}","",query)
        data = {"sentences":[(x)]}
        payload = str(data).replace("'","\"")
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=payload.encode('utf-8')) as r:
                r.raise_for_status()
                response = (await r.json())['emoji'][0]
        response.sort(reverse=True, key=lambda e: e['prob'])
        return [i for i in response[:results] if i['prob'] > min_prob]
    else:
        return []
