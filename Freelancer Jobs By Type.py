#%%
import pandas as pd
import requests as r
from bs4 import BeautifulSoup
import re
import matplotlib.pyplot as plt
from time import sleep
from threading import Thread
import numpy as np

data_ = None
#%%
def scrape_new_data():
    global data_
    url = "https://www.freelancer.in/job/"
    x = r.get(url)
    #%%

    soup = BeautifulSoup(x.content,'lxml')
    jobs = soup.find_all('li')
    all_jobs = []
    for each in jobs[:]:
        each = each.find('a')
        try:
            text = each.text.strip().replace('\xa0','').replace('\n\n','')
            c = re.findall(r'\(\d+\)', text)[-1]
            all_jobs.append([text.replace(c,''), int(c[1:-1])])
        except: 
            # print(text)
            pass
    # return all_jobs
    print('Yeah! Get the DATA!!')
    data_ = all_jobs
    


#%%
plt.ion()
old_counter = np.zeros(20)

def plot(data):
    global ax, fig, old_counter
    fig.canvas.flush_events()

    df = pd.DataFrame(data, index=None).sort_values(by=1, ascending=False)
    
    titles = df[0].head(20).to_list()
    counter = df[1].head(20).to_list()

    if any(old_counter):
        cc = np.array(counter) - old_counter
        print("Update:", cc)
    old_counter = counter.copy()
    # print(old_counter)

    ax.barh(titles[::-1], counter[::-1])
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.3,
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='grey')

    fig.canvas.draw()

# Figure Size
#fig, ax = plt.subplots(figsize =(6, 5))
##while True:
##    print("updating...",end='\r')
##    t = Thread(target=scrape_new_data)
##    t.start()
##    # t.join()
##    
##    plt.pause(3.0)
##    plot(data_)
##
##    sec = 10.0
##    print('Sleeping %s sec'%(int(sec)), end='\r')
##    plt.pause(sec)



# Save to CSV File
scrape_new_data()
df = pd.DataFrame(data_)
df = df.sort_values(by=1,ascending=False)
print(df.head(20).to_string(index=False, header=False))
df.to_csv("JOBS by Type.csv", header=['Job Name', 'Count'], index=False)

input()
# open output file in excel application
import os
os.system('start EXCEL.EXE "%s"'%("JOBS by Type.csv"))

