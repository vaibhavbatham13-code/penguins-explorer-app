import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df=pd.read_csv(r"C:\Users\ADMIN\Downloads\student_data.csv")

print(df)
df['Age']=pd.to_numeric(df['Age'])
df['Age']=df['Age'].fillna(df['Age'].mean())
print(df['Age'])

df['Height']=pd.to_numeric(df['Height'])
df['Height']=df['Height'].fillna(df['Height'].median())
print(df['Height'])

df['Weight']=pd.to_numeric(df['Weight'])
df['Weight']=df['Weight'].fillna(df['Weight'].median())
print(df['Weight'])

df['Grade']=df['Grade'].fillna(df['Grade'].mode()[0])
print(df['Grade'])

# MinMax Scaling
scaler = MinMaxScaler()

df[['Age', 'Height','Weight']] = scaler.fit_transform(df[['Age', 'Height', 'Weight']])

print("After MinMaxScaling:")
print(df)


print("Missing values:",df.isna().sum())
