import requests
from google.cloud import storage
from datetime import datetime
import pandas as pd

def api_to_gcs(url, filename):
  APP_TOKEN = "xxxxxxxxxxxxxxxxxxxx"
  headers = {'X-App-Token': APP_TOKEN,}
  response = requests.get(url, headers=headers).json()
  temp_df = pd.json_normalize(response)
  
  # Change the time to timestamp format so Tableau can read, then drop unnecessary columns
  time_col = [f"{i[:2]}:{i[2:]}" for i in temp_df["time_occ"]]
  date_col = temp_df["date_occ"].str[:10]
  temp_df["datetime_occured"] = pd.to_datetime(date_col + " " + time_col, format='%Y-%m-%d %H:%M:%S')
  temp_df = temp_df.drop(['location_1.human_address', 'time_occ'], axis=1)
  
  # Rename columns
  df = temp_df.rename({'date_rptd': 'date_reported', 'date_occ': 'date_occured', 'area': 'area_id',
       'rpt_dist_no': 'reporting_district_no', 'crm_cd': 'crime_code', 'crm_cd_desc': 'crime_code_description', 'mocodes':'mo_codes', 'vict_age':'victim_age',
       'vict_sex': 'victim_sex', 'vict_descent': 'victim_descent', 'premis_cd': 'premise_code', 'premis_desc': 'premise_description', 'location': 'address',
       'location_1.latitude':'latitude', 'location_1.longitude':'longitude'}, axis = 1)
  
  # temporarily remove 'time_occured' from df
  temp_column = df.pop('datetime_occured')
  
  # insert temp_column using insert(position,column_name,column_value) function (To reorder columns)
  df.insert(3, 'datetime_occured', temp_column)

  client = storage.Client(project='main-being-366219')
  bucket = client.get_bucket('la_traffic_2020')  
  blob = bucket.blob(filename)
  blob.upload_from_string(df.to_csv(index = False),content_type = 'csv')

def main(data, context):
  api_to_gcs("https://data.lacity.org/resource/d5tf-ez2w.json?$where=date_occ >= '2020-01-01T00:00:00'&$limit=250000", 
  "la_traffic_2020.csv")
