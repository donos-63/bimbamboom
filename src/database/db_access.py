from src.database.country_dto import Country
from pymongo import MongoClient
from src.configuration.resources import *
from datetime import datetime

class DatabaseManager:
    """Provide methods and connection to the MongoDb database
    """

    __CONNECTION_STRING = str.format("mongodb+srv://{}:{}@{}", MONGODB_USER, MONGODB_PASSWORD, MONGODB_SERVER)
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if DatabaseManager.__instance == None:
            DatabaseManager()
        return DatabaseManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DatabaseManager.__instance != None:
            raise Exception("This class is a singleton.")
        else:
            DatabaseManager.__instance = self
            print(DatabaseManager.__CONNECTION_STRING)
            self.__client = MongoClient(DatabaseManager.__CONNECTION_STRING)


    def _get_collection(self, db_name, collection_name):
        """Generic method to connect to a given collection in a given database
        If the database or the collection doesn't exist, it will be created.
        Args:
            db_name (str): name of the database.
            collection_name (str): name of the collection.
        Returns:
            collection: the collection.
        """
        return self.__client.get_database(db_name).get_collection(collection_name)


    def get_country_by_name(self, name) -> Country:
        """ Get a country by its name.
        Args:
            name (str): name of the country.
        Returns:
            json: the country.
        """
        name = str.lower(name)

        response = self._get_collection('countries_in_number', 'countries').find_one({'name': name})

        if response is None:
            response={"Message": "This country doesn't exist."}

        return response

    def set_country(self, name, country = None) -> Country:
        """ Add a new country to the databse with random informations if not set.
        Args:
            name (str): name of the country.
            country (Country): the country to add. None if random country
        Returns:
            json: data of the created country.
        """
        name = str.lower(name)

        if(country == None):
            country = Country()
            country.generate_random_country(name)

        self._get_collection('countries_in_number', 'countries').insert_one(country.to_json())

        return self.get_country_by_name(name)

    def delete_country_by_name(self, name) -> str:
        """Delete a country by its name.
        Args:
            name (str): name of the country.
        Returns:
            json: confirmation message.
        """

        name = str.lower(name)
        
        self._get_collection('countries_in_number', 'countries').delete_many({'name': name})

        return {"Message": "The country has been deleted."}


    def update_country_by_name(self, name, updated_data) -> Country:
        """Update a country by its name.
        Args:
            name (str): name of the country.
            data (dictionnary): list of key/value to update.
        Returns:
            json: updated country.
        """
        name = str.lower(name)

        filter = {"name": name}
        values = {"$set": updated_data}
        date = {"$set": {"update_date" : datetime.now().strftime(MONGODB_DATE_FORMAT)}}
                
        self._get_collection('countries_in_number', 'countries').update_one(filter, [values, date])

        return self.get_country_by_name(name)

    def get_countries_by_density(self, quarter1_v_low, quarter2_low, quarter3_medium ) -> str:
        """ Function that group countries by density

        Args:
            quarter1_v_low (int): first quarter between 0 and $quarter1_v_low (incl.)
            quarter2_low (int): second quarter between $quarter1_v_low and $quarter2_low (incl.)
            quarter3_medium (int): third quarter between $quarter2_low and $quarter3_medium (incl.)
	        [implicit] last_quarter: fourth quarter superior than $quarter3_medium        

        Returns:
            json: all the database's countries grouped by density ranges.
        """

        if quarter3_medium < quarter2_low or quarter2_low < quarter1_v_low:
            raise ValueError('bad quarters definition. Quarters must be superior to previously quarters')

        v_low_coll = self._get_collection('countries_in_number', 'countries').find({'density':{'$lte':quarter1_v_low}})
        low_coll = self._get_collection('countries_in_number', 'countries').find({'density': {'$gt' : quarter1_v_low, '$lte' : quarter2_low}})
        med_coll = self._get_collection('countries_in_number', 'countries').find({'density': {'$gt' : quarter2_low, '$lte' : quarter3_medium}})
        h_coll = self._get_collection('countries_in_number', 'countries').find({'density': {'$gt' : quarter3_medium}})

        return {'Poor density' : v_low_coll, 'Low density' : low_coll, 'Middle density' : med_coll, 'High density' : h_coll}

    def is_db_exists(self) -> bool:
        """ Test if project database exists

        Returns:
            bool: True if DB exists, else false
        """
        count = self._get_collection('countries_in_number', 'countries').count() > 0
        return count

    def drop_countries(self) -> None:
        self._get_collection('countries_in_number', 'countries').drop()
