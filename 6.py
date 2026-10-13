import pandas as pd
import  matplotlib.pyplot as plt
data ={"Age": [12,13,15,11,18,14,16,20]}

df = pd.DataFrame(data)
lb=['Child','Teenager','Adult']
df[('Age_Bins')]=pd.cut(df['Age'],bins = 3,labels= lb)
print(df)
plt.hist(df['Age_Bins'])
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.show()