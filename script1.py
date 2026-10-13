import pandas as pd
import matplotlib.pyplot as plt

df= pd.read_csv(r"C:\Users\ADMIN\Downloads\student_data.csv")

# Histogram
df['Age'].plot(kind='hist',bins=5)
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.title("Age Distribution")
plt.show()

#Box Plot
df['Age'].plot(kind='box')
plt.ylabel("Age")
plt.title("Age Box Plot")
plt.show()



