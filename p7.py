import pandas as pd
import matplotlib.pyplot as plt

data={"Age":[6,12,11,20,18,25,34]}
df=pd.DataFrame(data)
bin_boundary=[0,12,20,34,40]
bin_label=['child','teenager','adult','middel age']
df['Age_bin']=pd.cut(df['Age'],bins=bin_boundary,labels=bin_label)
print(df)

plt.hist(df['Age_bin'])
plt.xlabel("Age_bias")
plt.ylabel("Frequency")
plt.show()