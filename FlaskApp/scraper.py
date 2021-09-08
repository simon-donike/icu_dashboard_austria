# csv URL
url = "https://covid19-dashboard.ages.at/data/CovidFallzahlen.csv"

# read csv from URL
import pandas as pd
import geopandas as gpd
import numpy as np
df=pd.read_csv(url,sep=";")
df.to_csv("/var/www/FlaskApp/FlaskApp/data/covid_data.csv",sep=";",index=False)

# transforming timestamps to proper DateTime format
import datetime as dt
from datetime import datetime
import time
timestamps = []
for i in df["MeldeDatum"]:
    i = i.replace(".","")
    i = i.replace(":","")
    timestamps.append(dt.datetime.strptime(i, "%d%m%Y %H%M%S"))
df["MeldeDatum"] = timestamps
df = df.drop(["Meldedat"], axis=1)

# get List of State Names
states = list(df["Bundesland"].unique())

# append total hospitalizations to DF
l_temp = []
for a,b in zip(df["FZHosp"],df["FZICU"]):
    l_temp.append(a+b)
df["Hospitalizations_total"] = l_temp

# append total ICU capacity to DF
l_temp = []
for a,b in zip(df["FZICU"],df["FZICUFree"]):
    l_temp.append(a+b)
df["ICU_capacity"] = l_temp

# append ICU occupancy percentages to DF
l_temp = []
for a,b in zip(df["FZICU"],df["ICU_capacity"]):
    try:
        l_temp.append(100.0 * float(a)/float(b))
    except ZeroDivisionError:
        l_temp.append(0.0)
df["ICU_perc"] = l_temp

# create list of dataframes by Bundesland
ls_df = []
for i in states:
    temp = df[df["Bundesland"]==i]
    ls_df.append(temp)
    
# importing adm0 and adm1 shapefilesas geopandas dataframes
adm1 = gpd.read_file("/var/www/FlaskApp/FlaskApp/data/gadm36_AUT_1.shp")
adm0 = gpd.read_file("/var/www/FlaskApp/FlaskApp/data/gadm36_AUT_0.shp")

#writing to json
#adm1.to_file("data/austria_adm1.geojson", driver="GeoJSON")
#adm0.to_file("data/austria_adm0.geojson", driver="GeoJSON") 

# save CSV after manipulating & rounding
df = df.round(1)
df.to_csv("/var/www/FlaskApp/FlaskApp/data/ICU_data.csv")

# create most recent DF for map
most_recent_date = df['MeldeDatum'].max()
df2 = df.loc[df['MeldeDatum'] == most_recent_date]
df2.to_pickle("/var/www/FlaskApp/FlaskApp/data/df2.pkl")

# join geometries with most recent data per state
df_map =gpd.read_file("/var/www/FlaskApp/FlaskApp/data/austria_adm1.geojson")
df_map["Bundesland"] = df_map["NAME_1"]
df_map = pd.merge(df2,df_map,on="Bundesland")
df_map = gpd.GeoDataFrame(df_map, geometry="geometry")
df_map.to_pickle("/var/www/FlaskApp/FlaskApp/data/df_map.pkl")
# drop unused columns and save file in data folder
df_map.drop(["BundeslandID","GID_0","NAME_0","NAME_1","GID_1","VARNAME_1","NL_NAME_1","TYPE_1","ENGTYPE_1","CC_1","HASC_1","test_value"],axis=1).to_csv("/var/www/FlaskApp/FlaskApp/data/df_map.csv",index=False)


"""
CREATE DFs FOR UPDATE GRAPHS
"""
df_perc = pd.DataFrame({
    "MeldeDatum": np.asarray(df.loc[df['Bundesland'] == "Alle"]["MeldeDatum"]),
    "Alle": np.asarray(df.loc[df['Bundesland'] == "Alle"]["ICU_perc"]),
    "Burgenland": np.asarray(df.loc[df["Bundesland"] == "Burgenland"]["ICU_perc"]),
    "Kärnten": np.asarray(df.loc[df['Bundesland'] == "Kärnten"]["ICU_perc"]),
    "Niederösterreich": np.asarray(df.loc[df["Bundesland"] == "Niederösterreich"]["ICU_perc"]),
    "Oberösterreich": np.asarray(df.loc[df['Bundesland'] == "Oberösterreich"]["ICU_perc"]),
    "Salzburg": np.asarray(df.loc[df["Bundesland"] == "Salzburg"]["ICU_perc"]),
    "Steiermark": np.asarray(df.loc[df['Bundesland'] == "Steiermark"]["ICU_perc"]),
    "Tirol": np.asarray(df.loc[df["Bundesland"] == "Tirol"]["ICU_perc"]),
    "Vorarlberg": np.asarray(df.loc[df['Bundesland'] == "Vorarlberg"]["ICU_perc"]),
    "Wien": np.asarray(df.loc[df["Bundesland"] == "Wien"]["ICU_perc"]),
})
df_perc.to_pickle("/var/www/FlaskApp/FlaskApp/data/df_perc.pkl")

df_FZICU = pd.DataFrame({
    "MeldeDatum": np.asarray(df.loc[df['Bundesland'] == "Alle"]["MeldeDatum"]),
    "Alle": np.asarray(df.loc[df['Bundesland'] == "Alle"]["FZICU"]),
    "Burgenland": np.asarray(df.loc[df["Bundesland"] == "Burgenland"]["FZICU"]),
    "Kärnten": np.asarray(df.loc[df['Bundesland'] == "Kärnten"]["FZICU"]),
    "Niederösterreich": np.asarray(df.loc[df["Bundesland"] == "Niederösterreich"]["FZICU"]),
    "Oberösterreich": np.asarray(df.loc[df['Bundesland'] == "Oberösterreich"]["FZICU"]),
    "Salzburg": np.asarray(df.loc[df["Bundesland"] == "Salzburg"]["FZICU"]),
    "Steiermark": np.asarray(df.loc[df['Bundesland'] == "Steiermark"]["FZICU"]),
    "Tirol": np.asarray(df.loc[df["Bundesland"] == "Tirol"]["FZICU"]),
    "Vorarlberg": np.asarray(df.loc[df['Bundesland'] == "Vorarlberg"]["FZICU"]),
    "Wien": np.asarray(df.loc[df["Bundesland"] == "Wien"]["FZICU"]),
})
df_FZICU.to_pickle("/var/www/FlaskApp/FlaskApp/data/df_FZICU.pkl")

df_ICU_cap = pd.DataFrame({
    "MeldeDatum": np.asarray(df.loc[df['Bundesland'] == "Alle"]["MeldeDatum"]),
    "Alle": np.asarray(df.loc[df['Bundesland'] == "Alle"]["ICU_capacity"]),
    "Burgenland": np.asarray(df.loc[df["Bundesland"] == "Burgenland"]["ICU_capacity"]),
    "Kärnten": np.asarray(df.loc[df['Bundesland'] == "Kärnten"]["ICU_capacity"]),
    "Niederösterreich": np.asarray(df.loc[df["Bundesland"] == "Niederösterreich"]["ICU_capacity"]),
    "Oberösterreich": np.asarray(df.loc[df['Bundesland'] == "Oberösterreich"]["ICU_capacity"]),
    "Salzburg": np.asarray(df.loc[df["Bundesland"] == "Salzburg"]["ICU_capacity"]),
    "Steiermark": np.asarray(df.loc[df['Bundesland'] == "Steiermark"]["ICU_capacity"]),
    "Tirol": np.asarray(df.loc[df["Bundesland"] == "Tirol"]["ICU_capacity"]),
    "Vorarlberg": np.asarray(df.loc[df['Bundesland'] == "Vorarlberg"]["ICU_capacity"]),
    "Wien": np.asarray(df.loc[df["Bundesland"] == "Wien"]["ICU_capacity"]),
})
df_ICU_cap.to_pickle("/var/www/FlaskApp/FlaskApp/data/df_ICU_cap.pkl")

# Writing to logfile
file_object = open('/var/www/FlaskApp/FlaskApp/log.txt', 'a')
now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
file_object.write('Success:  '+date_time+"\n")
file_object.close()



"""

DB CONNECTOR

"""

# DB create string from csv for COVID data
import csv
with open('/var/www/FlaskApp/FlaskApp/data/covid_data.csv', 'r') as f:
    instr = ""
    reader = csv.reader(f,delimiter=";")
    #print(reader)
    next(reader) # Skip the header row.
    for row in reader:
        instr=instr+("INSERT INTO icu_data VALUES ('"+str(row[0])+"','"+str(row[1])+"','"+str(row[2])+"','"+str(row[3])+"','"+str(row[4])+"','"+str(row[5])+"','"+str(row[6])+"','"+str(row[7])+"','"+str(row[8])+"');" )                

# DB create string from csv for MAP data
import csv
import sys
csv.field_size_limit(sys.maxsize)
with open('/var/www/FlaskApp/FlaskApp/data/df_map.csv', 'r') as f:
    instr_map = ""
    reader = csv.reader(f,delimiter=",")
    #print(reader)
    next(reader) # Skip the header row.
    for row in reader:
        instr_map=instr_map+("INSERT INTO icu_map VALUES ('"+str(row[0])+"','"+str(row[1])+"','"+str(row[2])+"','"+str(row[3])+"','"+str(row[4])+"','"+str(row[5])+"','"+str(row[6])+"','"+str(row[7])+"','"+str(row[8])+"','"+str(row[9])+"','"+str(row[10])+"');" )

""" connecting to DB, parsing SQL statements """
def csv_parser(statement):
    import psycopg2
    return_ls = []
    try:
       connection = psycopg2.connect(user="icu_bot",
                                      password="5B2xwP8h4Ln4Y8Xs",
                                      host="85.214.150.208",
                                      port="5432",
                                      database="ICU")
       cursor = connection.cursor()
       sql_Query = statement
       #print(sql_Query)
       cursor.execute(sql_Query)
       connection.commit()
       #print("Selecting rows from mobile table using cursor.fetchall")
       #mobile_records = cursor.fetchall() 
       
       #print("Print each row and it's columns values")
       #for row in mobile_records:
       #    return_ls.append(list(row))
    
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL: ", error)
    
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            #print("PostgreSQL connection is closed")
    
    return return_ls


# update database in postgis
csv_parser("DELETE FROM icu_data")
csv_parser(instr)

# Update map data in server
csv_parser("DELETE FROM icu_map")
csv_parser(instr_map)



"""
GeoServer Connector
"""
try:
	df_geojson = pd.read_json("https://zgis187.geo.sbg.ac.at/geoserver/IPSDI_WT20/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=IPSDI_WT20%3Aicu_map&maxFeatures=50&outputFormat=application%2Fjson")
	df_geojson.to_pickle("/var/www/FlaskApp/FlaskApp/data/df_geojson.pkl")
except:
	print("an exception occured connecting to the geoserver")
