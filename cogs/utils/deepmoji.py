
import requests
import re

def get_emoji(query: str, url: str, min_prob: int = 0.05, results: int = 5) -> list:
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
        r = requests.post(url, data=payload.encode('utf-8'))
        r.raise_for_status()
        response = r.json()['emoji'][0]
        def get_prob(e):
            return e['prob']
        response.sort(reverse=True, key=get_prob)
        ret = []
        for i in response[:results]:
            if i['prob'] > min_prob: ret.append(i)
            else: return ret
        return ret
    else:
        return []
