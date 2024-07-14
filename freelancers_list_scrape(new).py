import requests as r
from concurrent.futures import ThreadPoolExecutor
import json
import os

from json_extract import GetValue2
from pprint import pp
import pandas as pd 


headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
    'baggage': 'sentry-environment=prod,sentry-release=bd5cab465afe4252d031db2f04625d6d00b51257,sentry-public_key=29cfb544702b48e0985e69cd3ef5e84f,sentry-trace_id=7153292d57aa42a98ac8faec8296415b',
    # 'cookie': '_tracking_session=5ee9398e-4ff0-eb43-d29a-508e30df8975; uniform_id_linked=linked; GETAFREE_NOTNEW=true; _hjSessionUser_1223449=eyJpZCI6ImI1YjRhM2JmLWZhNDQtNTAyNS05YmIyLTY5NTRjZDdhMWE2MiIsImNyZWF0ZWQiOjE3MDMzMzU2MjI1OTAsImV4aXN0aW5nIjp0cnVlfQ==; session2=1e520c9a02f9d679d590dc5a578a3272280328b008e3fd68474fd20f760af7a55bc782951b30c3d1; GETAFREE_LANGUAGE=en; _fbp=fb.1.1706538037880.1547619208; _ga_31ZQKFK760=deleted; fbm_120131118061981=base_domain=.freelancer.com; XSRF-TOKEN=fgwYEL0UgFRMl235BLw7SUqoKZA8g73bkOKf0NUrheuVkD0NpGUDtU6l8numkrxc; pdfcc=1; _hjSession_1223449=eyJpZCI6IjhiMDViYTQ0LTAxODktNDhiNC1iODBmLTg3ZjVlNjhiNjcwZSIsImMiOjE3MjA5MDQ4MzU4MTcsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowfQ==; _ga=GA1.2.f7e67c4e-ec32-f6ba-e079-86ccb88d92bc; _gid=GA1.2.1169595866.1720904837; GETAFREE_USER_ID=43079445; GETAFREE_AUTH_HASH_V2=RAem9IZjHZ3WkStEOWFyyz%2ByKRj9BHa0ZtcJJEYzjQY%3D; qfence=eyJhbGciOiJIUzI1NiIsInR5cCI6IkZyZWVsYW5jZXJcXEdBRlxcQ29yZVxcSldUXFxKV1QifQ.eyI0MzA3OTQ0NSI6MTcyMDkwNDg0MSwic3ViIjoicXVpY2tsb2dpbmZlbmNlIiwiaWF0IjoxNzIwOTA0ODQxfQ.3AWRpM-ZmKcILYyVaLPPRMnWCXljikU2sNS0lqcM0Qo; _gat_gtag_UA_223765_6=1; _ga_31ZQKFK760=GS1.1.1720904836.15.1.1720904937.20.0.0',
    'dnt': '1',
    'freelancer-app-build-timestamp': '1720425928',
    'freelancer-app-is-installed': 'false',
    'freelancer-app-is-native': 'false',
    'freelancer-app-locale': 'en',
    'freelancer-app-name': 'main',
    'freelancer-app-platform': 'web',
    'freelancer-app-version': 'gitRevision=bd5cab4, buildTimestampInSeconds=1720425928',
    'freelancer-auth-v2': '43079445;RAem9IZjHZ3WkStEOWFyyz+yKRj9BHa0ZtcJJEYzjQY=',
    'freelancer-tracking': '5ee9398e-4ff0-eb43-d29a-508e30df8975',
    'priority': 'u=1, i',
    'referer': 'https://www.freelancer.com/search/users?userSkills=13&page=5',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sentry-trace': '7153292d57aa42a98ac8faec8296415b-bbdbbd06e3e7f332',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}





offset = 100

def make_req(n):
    params = {
        'limit': '100',
        'offset': f'{n}',
        'rating': '1', # rating 1 and up
        'query': '',
        'skills[]': '13',
        'avatar': 'true',
        'country_details': 'true',
        'display_info': 'true',
        'job_ranks': 'true',
        'jobs': 'true',
        'location_details': 'true',
        'online_offline_details': 'true',
        'preferred_details': 'true',
        'profile_description': 'true',
        'pool_details': 'true',
        'qualification_details': 'true',
        'reputation': 'true',
        'status': 'true',
        'webapp': '1',
        'compact': 'true',
        'new_errors': 'true',
        'new_pools': 'true',
    }

    # url = f"https://www.freelancer.com/ajax/directory/getFreelancer.php?offset={n}&limit={offset}&skills[]=13"
    # x = r.get(url)

    x = r.get(  
        'https://www.freelancer.com/api/users/0.1/users/directory/',
        params=params,
        # cookies=cookies,
        headers=headers,
    )

    print((x, n))

    if x.status_code == 200:  
        freelancers = x.json()['result']['users']
        
        for k in freelancers: print(k['username'])

           
        page = n//offset + 1

        with open(f'./freelancer-{page}.json','w') as fp: 
            json.dump(x.json(), fp)

    else: print('Request Failed!!', n)


with ThreadPoolExecutor(12) as executor:
    # not getting any more data after 10k results

    executor.map(make_req, range(0, 9660, offset))   

# Total freelancers : 4,336,461
# freelancers with rating 1 and up: 9k

# make_req(9600)


# %%
'''
api call parameters

https://www.freelancer.com/api/users/0.1/users/directory/?limit=20&offset=20&query=&avatar=true&country_details=true&display_info=true&job_ranks=true&jobs=true&location_details=true&online_offline_details=true&preferred_details=true&profile_description=true&pool_details=true&qualification_details=true&reputation=true&status=true&webapp=1&compact=true&new_errors=true&new_pools=true
'''


# loop through json files and append to list
freelancers_list = []

dir_ = 'more_than_1_rating'
for i in os.listdir(dir_):
    print(i)
    with open(f'./{dir_}/{i}') as fp: 
        d = json.load(fp)['result']['users']
        freelancers_list.extend(d)



DATA =[] 

for _ in freelancers_list[:]:
    hh = GetValue2(_)
    print(_['username'])

    reputation = hh.get_values('entire_history')
    star= reputation.get('overall','')
    review = reputation.get('all','')
    earnings = reputation.get('earnings','')
    
    # print(hh.get_values('jobs'))
    jobs = [x['name'] for x in _.get('jobs',[])]

    qualifications = [x['description'] for x in _.get('qualifications',[])]
    try:
        timezone =hh.get_values('timezone').get('timezone')
    except: timezone = ''

    d ={
        "registration_date": hh.get_values('registration_date'),
        'username': hh.get_values('username'),
        'name': hh.get_values('public_name'),
        'email': hh.get_values('email'),
        'hourly_rate': hh.get_values('hourly_rate'),
        'earnings': earnings,
        'star': star,
        'total review': review,
        'jobs': '\n'.join(jobs),

        'tagline': hh.get_values('tagline'),
        'country': hh.get_values('country')[0]['name'],
        'city': hh.get_values('city'),
        'status': hh.get_values('status'),
        

        'primary_currency': hh.get_values('primary_currency')['code'],
        'timezone': timezone,
        'qualifications':qualifications,
        'profile_description': hh.get_values('profile_description'),
    
    }
    d['url'] ='https://www.freelancer.com/u/' + d['username']

    # pp(d)

    
    DATA.append(d)




df = pd.DataFrame(DATA)
df = df.drop_duplicates('username') # remove duplicates

from collections import Counter
df.star = df['star'].apply(lambda x: round(x, 1)) # round off rating value
# Counter(df.star)

df.to_excel('freelancers_list (1 and up star rating).xlsx', index=False)



