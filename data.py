from operator import index
import pandas as pd 

df = pd.DataFrame([1, 2, 3],index=None)
print(df)
df.to_csv('./hoge.csv')
df.to_csv('./fuga.csv', index=None)
df.to_csv('./piyo.csv', index=None, header=False)