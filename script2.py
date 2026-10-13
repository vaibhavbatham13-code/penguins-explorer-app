df=pd.read_csv(r"C:\Users\monik\Desktop\Features & Python\Features\Programs\SampleFile.csv")
print(df)

print("Total duplicates:", df.duplicated().sum())
df = df.drop_duplicates()
print("Total duplicates:", df.duplicates().sum())

df['Full_Name'] = df['Full_Name'].str.strip()
df['Phone_Number'] = df['Phone_Number'].astype(str).str.strip()

df.to_csv('new.csv')



