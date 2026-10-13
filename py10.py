import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')

data={'Text':['Product is very goodddddd','Cloth quality is good:)','Experience is amazing']}
df=pd.DataFrame(data)
df['token']=df['Text'].apply(lambda x : word_tokenize(str(x)))

print(df)