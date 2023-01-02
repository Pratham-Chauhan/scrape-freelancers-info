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

        with open(f'./freelancer-{page}.json','w') as fp: 
            json.dump(x.json(), fp)

    else: print('Request Failed!!', n)


with ThreadPoolExecutor() as executor:
    # first 10,000 results are possible only
    executor.map(make_req, range(0, 10000, offset))   

# Total freelancers : 4,336,461


'''
api call parameters

https://www.freelancer.com/api/users/0.1/users/directory/?limit=20&offset=20&query=&avatar=true&country_details=true&display_info=true&job_ranks=true&jobs=true&location_details=true&online_offline_details=true&preferred_details=true&profile_description=true&pool_details=true&qualification_details=true&reputation=true&status=true&webapp=1&compact=true&new_errors=true&new_pools=true
'''