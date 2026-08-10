import pandas as pd

df = pd.read_csv('/Users/mushood/Documents/code/personal/coeus/04_RESOURCES/Career/SP_-_Worker_and_Temporary_Worker_Web_Register_-_2026-07-17.csv')
print('Shape:', df.shape)
print('Columns:', df.columns.tolist())
print('Sample:')
print(df.head(10).to_string())
print('\nType & Rating values:')
print(df['Type & Rating'].value_counts().head(20))
print('\nRoute values:')
print(df['Route'].value_counts())
print('\nTown/City sample:')
print(df['Town/City'].value_counts().head(20))