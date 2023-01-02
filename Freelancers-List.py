import requests as r
from concurrent.futures import ThreadPoolExecutor
import json

offset = 100

def make_req(n):
    url = f"https://www.freelancer.in/ajax/directory/getFreelancer.php?offset={n}&limit={offset}"
    x = r.get(url)
    print((x, n))

    if x.status_code == 200:     
        page = n//offset + 1

        with open(f'./json_data/freelancer-{page}.json','w') as fp: 
            json.dump(x.json(), fp)

    else: print('Request Failed!!', n)

    
with ThreadPoolExecutor() as executor:
    executor.map(make_req, range(0, 10000, offset))    

# Total freelancers : 4,336,461

