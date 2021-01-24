# Le client est roi  

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
  * [Routes](#routes)
  * [Settings](#settings)

<!-- ABOUT THE PROJECT -->
## About The Project

### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com)
* [PyMongo](https://pymongo.readthedocs.io)

<!-- GETTING STARTED -->
## Getting Started

Get a local copy up and running following these steps.

### Installation

1. Clone the repository :

    ```sh
    git clone https://github.com/donos-63/bimbamboom
    ```
    
2. Update db connexion informations in [src/configuration/resources.py](https://github.com/donos-63/bimbamboom/blob/main/src/configuration/resources.py)
 * The current project is given with authentication keys to Atlas MongoDb provider
3. Install the requirements :
    ```sh
    pip install -r requirements.txt
    ```
4. Run the initialisation script [init_db.py](https://github.com/donos-63/bimbamboom/blob/main/init_db.py)

<!-- USAGE EXAMPLES -->
## Usage

* Run [main.py](https://github.com/donos-63/bimbamboom/blob/main/main.py) to start the flask server.  
  * The API will be launched on port 8080.
* Open [test.ipynb](https://github.com/donos-63/bimbamboom/blob/main/test.ipynb) to read the API tests and make some new ones.  


### Routes
* ```/api/country/<name>``` *(**GET** method, name:str)* get a country by its name.  
* ```/api/insert_random/<name>``` *(**GET** method, name:str)* add a randomly created country to the database.    
* ```/api/delete``` *(**DELETE** method)* delete a country .  
* ```/api/update``` *(**POST** method)* update data from a country.  
* ```/api/density``` *(**POST** method)* group countries by density. 

### Settings
* [configuration > resources.py](https://github.com/donos-63/bimbamboom/blob/main/src/configuration/resources.py) contains the connection settings and environment variables.   
* [database > db_access.py](https://github.com/donos-63/bimbamboom/blob/main/src/database/db_access.py) provides the methods and connection to the MongoDb database.

