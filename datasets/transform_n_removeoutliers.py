import pandas as pd

# df_interactions = pd.read_csv("datasets/RAW_interactions.csv")
df_recepies = pd.read_csv("RAW_recipes_removena.csv")

# converting nutrients to seperate columns
df_recepies['nutrition_list'] = df_recepies['nutrition'].str[1:-1].str.split(',')
seperate_columns = ['Calories', 'TotalFat', 'Sugar', \
    'Sodium', 'Protein', 'SaturatedFat', 'Carbohydrates']
df_recepies_split = pd.DataFrame(df_recepies['nutrition_list'].tolist() , columns=seperate_columns)

#concatinating the newly created columns with the ones that was previously there
df_recepies_split = pd.concat([df_recepies, df_recepies_split], axis=1)

#the newly created columns were in type string so converting them to float
df_recepies_split[seperate_columns] = df_recepies_split[seperate_columns].astype(float)

#calculating mean and standard deviation of numeric columns
# mean = df_recepies_split[numeric_columns].mean()
# sd = df_recepies_split[numeric_columns].std()

#listing the columns which has numeric values
numeric_columns = ['Calories', 'TotalFat', 'Sugar', 'Sodium', 'Protein',\
     'SaturatedFat', 'Carbohydrates', 'n_steps', 'n_ingredients', 'minutes']

def check_outlier(df):
    for column in numeric_columns:
        print(df[column].mean() , df[column].std())
        upper = df[column] < df[column].mean()+3*df[column].std()
        lower = df[column] > df[column].mean()-3*df[column].std()
        df = df[upper&lower]
    return df

df = check_outlier(df_recepies_split)
mask1 = df['Calories'] <= 2000
mask2 = df['minutes'] < 500
df = df[mask1&mask2]
df = df.drop(['contributor_id', 'submitted', 'tags'], axis=1)
print(df.shape)
print(df.info())
df.to_csv('Transformed_recipes.csv')
# print(mean_minutes)

#this function checks the outlier using mean +- 3sd ,and replaces the outlier with the exteme values 
    # df = df[df.std  >  ]
    
    # for ind,row in df.iterrows():
    #     for i,(x,y) in enumerate(zip(mean,sd)): 
    #         upper_limit = x + 3*y 
    #         lower_limit = x - 3*y
    #         if row[numeric_columns[i]] > upper_limit or row[numeric_columns[i]] < lower_limit:
    #             df = df.drop(ind)
    #             break
    # # df.drop(df[df[numeric_columns[i]] < lower_limit].index, inplace=True)
    # # df.drop(df[df[numeric_columns[i]] < lower_limit].index, inplace=True)
    #             # df_recepies_split.at[ind,numeric_columns[i]] = random.randint(df_recepies_split[numeric_columns[i]].min(), int(upper_limit))
              
            

    #             # df_recepies_split.at[ind,numeric_columns[i]] = random.randint(df_recepies_split[numeric_columns[i]].min(), int(upper_limit))