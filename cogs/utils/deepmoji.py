
# from time import time
import requests
import re

def get_emoji(query: str, url: str, min_prob: int = 0.05, results: int = 5):
    x = re.sub("[<>:'\"]|\d{5,}","",query)
    # start = time()
    # print(f'Sending {x} to Deepmoji API')
    data = {"sentences":[(x)]}
    payload = str(data).replace("'","\"")
    r = requests.post(url, data=payload.encode('utf-8'))
    # print(f'Got API response after {round(time()-start,2)}s')
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