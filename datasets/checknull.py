import pandas as pd


df_recepies = pd.read_csv("RAW_recipes.csv")
print(df_recepies.shape)
print(df_recepies.info())

# get_na_count(df_interactions)
# def check_count(df):
#     for ind,row in df.iterrows():
#         if len(row['nutrition']) != 7:
#             return row['id']
print(df_recepies.isna().sum())
mask = df_recepies['name'] != ''
#replace '' with Unknown
df_recepies.fillna(value = 'Unknown', inplace = True) 
print(df_recepies.isna().sum())
df_recepies.to_csv('RAW_recipes_removena.csv')



# def check_type(df):
#     for ind,row in df.iterrows():
#         print(type(row['nutrition']))
#         break


