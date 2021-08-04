from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

soup = BeautifulSoup(requests.get('https://content.codecademy.com/courses/beautifulsoup/cacao/index.html').content, 'html.parser')

rating_data = soup.find_all(attrs={"class": "Rating"})
ratings = []
for rating in rating_data[1:]:
  ratings.append(float(rating.text))

company_data = soup.select('.Company')
companies = []
for company in company_data[1:]:
  companies.append(company.get_text())

cocoa_data = soup.find_all(attrs={"class": "CocoaPercent"})
cocoa = []
for coco in cocoa_data[1:]:
  percent = (int(float(coco.get_text().strip('%'))))
  cocoa.append(percent)

d = {"Company": companies, "Ratings": ratings, "CocoaPercentage": cocoa}

df = pd.DataFrame.from_dict(d)
mean_vals = df.groupby("Company").Ratings.mean()
ten_best = mean_vals.nlargest(10)

plt.scatter(df.CocoaPercentage, df.Ratings)

z = np.polyfit(df.CocoaPercentage, df.Ratings, 1)
line_function = np.poly1d(z)
plt.plot(df.CocoaPercentage, line_function(df.CocoaPercentage), "r--")

plt.xlabel('Cocoa Percentage')
plt.ylabel('Chocolate Rating')
plt.show()
