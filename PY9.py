import pandas as pd
import numpy as np

data={"Distance":[2000,3000,4000,5000,6000]}

df=pd.DataFrame(data)
df['distance_log'] = np.log1p(df['Distance']).round(2)
print(df)