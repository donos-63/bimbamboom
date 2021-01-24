from src.database.db_access import DatabaseManager
from src.database.country_dto import Country
import pandas as pd
import os

data_folder = os.path.join(os.getcwd(), "src", "data", "in", "countries_data.csv" )

#Simple code to load countries dataset to mongodb db
db_exists = DatabaseManager.getInstance().is_db_exists()
if db_exists:
    print("database already exists: drop it")
    DatabaseManager.getInstance().drop_countries()

df  = pd.read_csv(data_folder, sep=',', decimal='.')
#simplify columns name
df = df.rename(columns={"Country (or dependency)": "name", "Population (2020)": "population", "Yearly Change": "yearly_change", "Net Change": "net_change", "Density (P/Km²)": "density", "Land Area (Km²)": "land_area", "Migrants (net)": "migrants", "Fert. Rate": "fertilisation_rate", "Med. Age": "med_age", "Urban Pop %": "urban_pop", "World Share": "world_share"})
#fill N.A columns with None values
cols = ["population", "yearly_change", "net_change", "density", "land_area", "migrants", "fertilisation_rate", "med_age", "urban_pop", "world_share"]
df[cols] = df[cols].replace('N.A.',None)

#loop on records 
print("start loading data to database")
for index, row in df.iterrows():
    c = Country()
    #initialize country instance
    c.initialize_country(row['name'], row['population'], row['yearly_change'].replace(" %", ''), row['net_change'], row['density'], row['land_area'], row['migrants'], row['fertilisation_rate'], row['med_age'], row['urban_pop'].replace(" %", ''), row['world_share'].replace(" %", ''))
    #insert in db
    DatabaseManager.getInstance().set_country(row['name'], c)

print('database initialisation completed')
