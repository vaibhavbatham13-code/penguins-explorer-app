import pandas as pd
df = pd.read_csv(r"C:\Users\ADMIN\Downloads\customer_data.csv")

print(df.head())
print("Total duplicates:",df.duplicated().sum())
df=df.drop_duplicates()
print("Total duplicates:",df.duplicated().sum())
df['Full_Name']=df['Full_Name'] .str.strip()
df['Phone_Number']=df['Phone_Number'].astype(str).str.strip()
df.to_csv('new.csv')
df['Joining_Date']=pd.to_datetime(df['Joining_Date'], format='%d-%m-%y', errors='coerce')
df['Joining_Date']=df['Joining_Date'].dt.strftime('%m-%B-%Y')
df['Salary_INR']=df['Salary_INR'].astype(str).replace(r"\D","",regex=True)
df['Salary_INR']=pd.to_numeric(df['Salary_INR'])
print("Missing Values:", df.isna().sum())
print (df['Salary_INR'])
df['Salary_INR']=df['Salary_INR'].fillna(df['Salary_INR'].median())
print(df['Salary_INR'])
print(df)




