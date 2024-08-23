Vincent MAYMARD
2024-08-19 Web Parser and streamlit app for the Paris 2024 Marathon Result Website

Credits to Jean MILPIED for providing the methology for this project in his Linkedin post dated 24-08-16:
https://www.linkedin.com/posts/jeanmilpied_marathonpourtous-paris2024-activity-7230099336288702465-cFf3?utm_source=share&utm_medium=member_desktop

Source website: https://paris-mpt.r.mikatiming.de/2024/?pid=start&pidp=tracking
Jean Milpied's streamlit App: https://marathon-pour-tous-paris-jo-2024.streamlit.app/

The MarathonScrapper file sends fake form requests to the 2024 Marathon Official website and saves the responses in a parquet file.
The MarathonCleaner file formats the response from the parquet file and calculates metrics of interest
The MarathonStreamlit file displays the information of interest on a Streamlit App
