import numpy as nd
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures

data ={'Study_Hour':[1,2,3,4,5],
       'Sleeping_Hour':[2,4,6,8,10]
       }
data = pd.DataFrame(data)
poly=PolynomialFeatures(degree=2,interaction_only=False)
poly.fit(data)
print(data)
print(poly.transform(data))
