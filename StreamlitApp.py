import os
import pandas as pd
import streamlit as st

from pandas import notna

# Open the saved dataframe from the Parquet file
filepath = os.path.join(os.getcwd(), "ScrappedData", "CleanedMarathonResults.parquet")
df = pd.read_parquet(path=filepath)
df['BrutTime'] = df['BrutTime'].dt.strftime("%H:%M:%S")
df['NetTime'] = df['NetTime'].dt.strftime("%H:%M:%S")

# Displays the App Title
st.image('banner.jpg')
st.title("PARIS 2024 - Marathon Results")
st.markdown('___')

# Requests a runner number input from the user
st.markdown(
    """
    <style>
    .large-label {
        font-size: 16px;
        font-weight: bold;
    }
    </style>
    <div class="large-label">Input a Runner Number:</div>
    """,
    unsafe_allow_html=True
)
st.number_input("", key="no", min_value=1, max_value=3000, value=1, step=1)

# Checks the validity of the input and returns the Brut Runner time and rank
prompt = ""
prompt_save = ""
validInput = 1
error = False
try:
  validInput = int(st.session_state.no)
except ValueError:
  prompt = "Please input a number"
  error = True
except:
  prompt = "Unknown error"
  error = True

hideNetTime = False
if not error:
  brutRunnerRank = df.loc[df['RunnerNumber'] == validInput, 'BrutRunnerRank']
  brutRunnerP = df.loc[df['RunnerNumber'] == validInput, 'BrutRunner%']
  brutTime = df.loc[df['RunnerNumber'] == validInput, 'BrutTime']

  if len(brutRunnerRank) * len(brutTime) * len(brutRunnerP) > 0:
    brutRunnerRank = int(brutRunnerRank.iloc[0])
    brutTime = brutTime.iloc[0]
    brutRunnerP = int(brutRunnerP.iloc[0])

    prompt = f"Runner #{st.session_state.no} ranked {brutRunnerRank} out of {len(df)} finishers in the Paris 2024 Marathon (Top {brutRunnerP}%)."
    prompt = prompt + "  \n\n"
    prompt_save = f"**Brut Time:** {brutTime} (Time of Reference) "
  else:
    prompt = f"There was either no runner with the number {st.session_state.no} or this runner did not finish the race"
    hideNetTime = True

st.write(prompt)

# Adds the net time to the prompt if available
prompt = ""
if not error:
  netTime = df.loc[df['RunnerNumber'] == validInput, 'NetTime']
  if len(netTime) > 0 and notna(netTime.iloc[0]):
    netTime = netTime.iloc[0]
    prompt = prompt_save + "  \n" +  f"**Net Time:** {netTime} (For information only)"
  else:
    prompt = prompt_save + "  \n" + f"Unfortunately, the net time of this runner is not available."

if not hideNetTime: st.write(prompt)

# Adds the Top 10 Runner Ranking
st.markdown('___')
if st.toggle("Show Leaderboard"):
  top10 = df.sort_values(by='BrutRunnerRank').iloc[0:9][['RunnerNumber', 'BrutRunnerRank', 'BrutTime', 'NetTime']]
  top10.columns = ['Runner Number', 'Runner Rank', 'Brut Time', 'Net Time']
  html = top10.to_html(index=False)
  html = f"""
  <div style="display: flex; justify-content: center;">
      {html}
  </div>
  """
  st.markdown(html, unsafe_allow_html=True)

st.markdown('___')

st.write("*This is an unofficial website on the Paris 2024 Olympic Marathon. For official results, please refer to:  \n"
         "[Paris 2024 Marathon Official Results](https://paris-mpt.r.mikatiming.de/2024/?pid=tracking&pidp=tracking)*")
