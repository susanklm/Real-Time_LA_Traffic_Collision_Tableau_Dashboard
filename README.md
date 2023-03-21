# Real-Time LA Traffic Collision Tableau Dashboard

This is a project that I did at Hack for LA. The purpose of this project is to create a real-time LA traffic collision Tableau dashboard by integrating Tableau with Google BigQuery. The steps are as follows:
1. Wrote a Python Google Cloud Function to download LA traffic collision data from 2020 until present from [data.lacity.org](https://data.lacity.org/Public-Safety/Traffic-Collision-Data-from-2010-to-Present/d5tf-ez2w). See [function-source](https://github.com/susanklm/Real-Time_LA_Traffic_Tableau_Dashboard/tree/main/function-source) for the Python code.
2. Set a Google Cloud Scheduler to download the traffic collision data into Google Cloud Storage every Tuesday noon. The target type was set to Pub/Sub.
3. Used SQL queries in Google BigQuery (which is connected to Google Cloud Storage) to do exploratory analyses and fix data quality issues. In this case the null values of victim age, victim descent, and victim sex were replaced with values based on the proportions of non-null victim age, victim descent, and victim sex. See the SQL query [here](https://console.cloud.google.com/bigquery?sq=80051879961:67e7eb9370ac4514b02333b3896a87ca).  
4. Scheduled the query from the previous step to run every Tuesday about 5 minues past noon. 
5. Integrated Tableau with BigQuery to create the real-time dashboard.

## Below are the links to the dashboards
There are two version of dashboards:
- [First version](https://public.tableau.com/app/profile/susan.kolim/viz/la_traffic_2020_realtime/LATraffic?publish=yes): The dashboard excludes the rows where victim age, victim descent, and victim sex are null.
- [Second version](https://public.tableau.com/app/profile/susan.kolim/viz/la_traffic_2020_realtime_v2/LATraffic): The dashboard includes the rows where victim age, victim descent, and victim sex are null by replacing the null values with values based on the proportions of non-null values. 
