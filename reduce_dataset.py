import pandas as pd

file_path = "training.1600000.processed.noemoticon.csv"

# Load only sentiment + text column
df = pd.read_csv(
    file_path,
    encoding="latin-1",
    header=None,
    usecols=[0, 5],   # sentiment, tweet text
    names=["sentiment", "tweet"]
)

print(df.head())

# Map sentiment
df['sentiment'] = df['sentiment'].map({
    0: 'Negative',
    4: 'Positive'
})


df_neg = df[df['sentiment'] == 'Negative'].sample(20000)
df_pos = df[df['sentiment'] == 'Positive'].sample(20000)

df_final = pd.concat([df_neg,df_pos])


print(df_final['sentiment'].value_counts())

df_final.to_csv("tweets_60k.csv", index=False)
print(" Reduced dataset saved")
df = pd.read_csv("tweets_60k.csv")

