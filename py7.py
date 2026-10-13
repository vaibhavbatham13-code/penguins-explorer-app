import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    "Hours_studied" : [2,4,6,8,10],
    "Marks" : [40,50,65,80,95],
    "Attendance" :[60,70,75,85,90]
}

df = pd.DataFrame(data)

print(df)

corr = df.corr()

print(corr)

sns.heatmap(corr, annot=True,cmap="coolwarm")
plt.show()