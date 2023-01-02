import os
import json
import pandas as pd

input_dir = "json_data"


ALL_DATA = []
for file in os.listdir(input_dir):
    fp = open(f"./{input_dir}/{file}", encoding='utf-8')
    data = json.load(fp)['users']
    fp.close()

    print(file)
    for u in data:
        name = u["public_name"]
        username = u['username']
        hourlyrate = u['hourlyrate']
        tagline = u['tagline']
        earning = u.get('total_earnings','')
        full_desc = u['profile']
        country = u['country']
        city = u['city']
        url = "https://www.freelancer.com"+u['profile_url']
        

        review_a = u.get('no_reviews','')
        eh_stars = u.get('eh_stars')
        rating = u['rating_stars_count']
        
        ALL_DATA.append([url, name, username, hourlyrate, earning, country, city, review_a, eh_stars, rating, tagline, full_desc])

df = pd.DataFrame(ALL_DATA, columns=['Url','Name','Username', 'hourlyrate','earning','country','city','review_a', 'eh_stars', 'rating','tagline','full_desc'])
df.to_excel('output.xlsx', index=False)

