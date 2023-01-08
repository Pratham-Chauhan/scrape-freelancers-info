import pandas as pd
df = pd.read_excel('./output.xlsx')

df.city = df.city.str.capitalize()
df.country = df.country.str.capitalize()

df_1 = df.groupby(['country','rating']).count()[['Name']].sort_values('Name', ascending=False).reset_index()
df_1

# only interested in top 5 countries
top_10_countries = df_1.country.unique()[:5]
# freelancer of top countries by rank
top_country_freelancer = df_1[df_1.country.isin(top_10_countries)].sort_values(['country','rating'], ascending=False)
top_country_freelancer


import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline
fig = plt.figure()
ax = fig.add_subplot(111)

# Create a figure and an Axes object
# fig, ax = plt.subplots()

for rating in [4.1,4.6,5.0]:# np.linspace(4,5,11):
    print('rating:', rating)
    data = top_country_freelancer[top_country_freelancer.rating==rating]
    # print(data)
    
    # data.plot(kind='bar',x='country',y='Name', ax=ax,color='r')
    ax.bar(data.country, data.Name)
    
fig.show()