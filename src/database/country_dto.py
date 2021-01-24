import random as rd
from datetime import datetime
from src.configuration.resources import *


class Country():

    def _rand_decimal(min, max, precision= 2) -> float:
        precision = 10^precision
        return rd.randint(min * precision, max * precision) / precision

    def generate_random_country(self, name : str):
        self.name = str.lower(name)
        self.pop_total = rd.randint(500,2000000000) #population between 10k to 3b
        self.yearly_change =  Country._rand_decimal(-10, 10) #yearly population change in %. Limited to 10%
        self.net_change = (int)(self.pop_total * self.yearly_change / 100) #yearly population number change, based on population and yearly change in %
        self.pop_density = rd.randint(1,30000) #population per km²
        self.land_area = (int)(self.pop_total/self.pop_density) #land area in Km²
        self.migrant_variation = rd.randint(1, (int)(self.pop_total*10/100)) #number of migrants variation in 1 year, limited to 10% of the total amount of residents
        self.fertilisation_rate = Country._rand_decimal(0, 8)
        self.middle_age = rd.randint(30, 70) #age average between 30 and 70 years old
        self.urban_pop = rd.randint(1, 99) #urban population in % between 1 and 99
        self.world_share = Country._rand_decimal(0, 50) #world share between 0 and 50%


    def to_json(self) -> str :

        json =  {"name": str.lower(self.name), 
                    "population": self.pop_total, 
                    "yearly_change": self.yearly_change, 
                    "net_change": self.net_change, 
                    "density" : self.pop_density,
                    "land_area" : self.land_area,
                    "migrants" : self.migrant_variation,
                    "fertilisation_rate" : self.fertilisation_rate,
                    "medium_age" : self.middle_age,
                    "urban_pop" : self.urban_pop,
                    "world_share" : self.world_share,
                    "update_date" : datetime.now().strftime(MONGODB_DATE_FORMAT)
                    }

        return json

    def initialize_country(self, name : str, population : int , yearly_change: float, net_change : int, density : int, land_area : int, migrants, fertilisation_rate : float, med_age : int, urban_pop : float, world_share : float):
        self.name = str.lower(name)
        self.pop_total = population
        self.yearly_change = float(yearly_change) if yearly_change is not None else None 
        self.net_change = net_change
        self.pop_density = density
        self.land_area = land_area
        self.migrant_variation = migrants
        self.fertilisation_rate = float(fertilisation_rate) if fertilisation_rate is not None else None 
        self.middle_age = int(med_age) if med_age is not None else None 
        self.urban_pop = float(urban_pop) if urban_pop is not None else None 
        self.world_share = float(world_share) if world_share is not None else None 
