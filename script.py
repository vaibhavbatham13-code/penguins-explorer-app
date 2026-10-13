import pandas as pd
import matplotlib.pyplot as plt
df=pd.read_csv(r"C:\Users\ADMIN\Downloads\student_data.csv")
plt.plot(df['Age'],
df['Height'])
plt.xlabel("Age")
plt.ylabel("Height")
plt.title("Age vs Height")
plt.show()
