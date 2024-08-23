import os
import pandas as pd
import numpy as np

# Open the saved dataframe from the Parquet file
filepath = os.path.join(os.getcwd(), "ScrappedData", "MarathonResults.parquet")
df = pd.read_parquet(path=filepath)

# Filter out all unassigned runner numbers
df = df[df["ParseStatus"] == "OK"]

# Convert the date columns to the datetime format
df['NetTime'] = pd.to_datetime(df['NetTime'], errors='coerce', format="%H:%M:%S")
df['BrutTime'] = pd.to_datetime(df['BrutTime'], errors='coerce', format="%H:%M:%S")
print(df.info())
print()

# Filter out all runners with no Net or Brut Time and checks cases where only one of these times is available
df["Status"] = "Net and Brut Time available"
df.loc[df["NetTime"].isna() & df["BrutTime"].notna(), "Status"] = "No Net Time"
df.loc[df["NetTime"].notna() & df["BrutTime"].isna(), "Status"] = "No Brut Time"
df.loc[df["NetTime"].isna() & df["BrutTime"].isna(), "Status"] = "No Net or Brut Time"
df = df.loc[df["Status"] != "No Net or Brut Time"]
df.reset_index(drop=True, inplace=True)
print(df.groupby('Status').size())
print()

# Determine the rank of each runner in the race and its %
df['BrutRunnerRank'] = (df["BrutTime"].rank(ascending=True, method='min')).astype(int)
brutTimes = df[df["BrutTime"].notna()].shape[0]
df['BrutRunner%'] = np.ceil(100*df['BrutRunnerRank']/brutTimes).astype(int)

df['NetRunnerRank'] = (df.loc[df["NetTime"].notna(), "NetTime"].rank(ascending=True, method='min'))
df['NetRunnerRank'] = df['NetRunnerRank'].fillna(-1)
df['NetRunnerRank'] = df['NetRunnerRank'].astype(int)
netTimes = df[df["NetTime"].notna()].shape[0]
df['NetRunner%'] = np.ceil(100*df['NetRunnerRank']/netTimes).astype(int)
df.loc[df['NetRunnerRank'] == -1, 'NetRunner%'] = -1

print(df.loc[df['NetRunnerRank'] == -1])
print(df)