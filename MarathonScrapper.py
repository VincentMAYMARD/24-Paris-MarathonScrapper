# Vincent MAYMARD
# 2024-08-19 Web Parser from the Paris 2024 Marathon Result Website

# Credits to Jean MILPIED for providing the methology for this project in his Linkedin post dated 24-08-16:
# https://www.linkedin.com/posts/jeanmilpied_marathonpourtous-paris2024-activity-7230099336288702465-cFf3
# ?utm_source=share&utm_medium=member_desktop

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def web_parser(url, form_data):
    # Send a GET request to the URL
    response = requests.post(url, form_data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finds the element that contains the Net Time
        net_time = soup.find(name='td', attrs={'class': 'f-time_finish_netto last'})
        brut_time = soup.find(name='td', attrs={'class': 'f-time_finish_brutto last'})

        if net_time and brut_time:
            net_time = net_time.get_text().strip()
            brut_time = brut_time.get_text().strip()
            return {"RunnerNumber": formData['search[start_no]'] ,"NetTime": net_time, "BrutTime": brut_time, "ParseStatus": "OK"}
        else:
            return {"RunnerNumber": formData['search[start_no]'] ,"NetTime": None, "BrutTime": None,
                    "ParseStatus": "RunnerNotFoundException"}
    else:
        return {"RunnerNumber": formData['search[start_no]'] ,"NetTime": None, "BrutTime": None,
                    "ParseStatus": "UnsuccessfulRequestException"}


# Query Parameters
MarathonUrl = "https://paris-mpt.r.mikatiming.de/2024/?pid=search&pidp=tracking"
formData = {
    'lang': 'EN_CAP',
    'startpage': 'start_responsive',
    'startpage_type': 'search',
    'event': 'MPT',
    'search[start_no]': 0,
    'submit': ''
}

# Response
df = {"RunnerNumber":[], "NetTime": [], "BrutTime": [], "ParseStatus": []}
filepath = os.path.join(os.getcwd(), "ScrappedData", "MarathonResults.parquet")
startTime = time.time()

for n in range(1, 25000):
    formData['search[start_no]'] += 1
    SiteResponse = web_parser(MarathonUrl, formData)
    for key, value in df.items():
        df[key] = value + [SiteResponse[key]]
    if n % 200 == 0:
        df_save = pd.DataFrame(df)
        df_save.to_parquet(filepath, index=False)
        elapsedTime = time.time() - startTime
        print(f"{elapsedTime:.0f}s - Saved the first {n} runners to the MarathonResults parquet file")
