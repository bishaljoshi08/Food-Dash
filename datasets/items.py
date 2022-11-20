import pandas as pd

df = pd.read_csv('Transformed_recipes.csv')
df["ingredients"] = df["ingredients"].apply(eval)

def to_1D(series):
    return pd.DataFrame([ x for _list in series for x in _list])

df = to_1D(df['ingredients']).value_counts().rename_axis('ingredient').reset_index(name='count')
print(df.info())
df.to_csv('ingredients_count.csv')