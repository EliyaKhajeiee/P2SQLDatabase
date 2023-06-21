#this is a class I am going to be doing all my country stuff in

import p2app.events
import sqlite3
from collections import namedtuple

Country = namedtuple(
    'Country',
    ['country_id', 'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'])


class Country_manager:
    """Class to have all my country data split up"""
    def __init__(self,cont_obj,db_path):
        """Initialize my data which I need to use"""
        self.cont_obj = cont_obj #Sent by view  : StartContinentSearchEvent: continent_code = 'EK', name = 'EliyaKhajeie'
        self.db_path = db_path

    def start_country_search_event(self):
        """Start the search for my country which yields back the necessary data depending on what you input in the GUI"""
        country_code = self.cont_obj.country_code()
        country_name = self.cont_obj.name()

        if country_name is None and country_code is not None:  # just the cont code
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM country WHERE country_code = ?", (country_code,))
            data_list = var.fetchall()
            for x in data_list:
                country_id = x[0]
                country_code = x[1]
                country_name = x[2]
                cont_id = x[3]
                wiki = x[4]
                kw = x[5]
                country = Country(country_id, country_code, country_name, cont_id, wiki,
                                  kw)
                yield p2app.events.CountrySearchResultEvent(country)
            connection.close()

        elif country_name is not None and country_code is None:  # just the country name
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM country WHERE name = ?", (country_name,))
            data_list = var.fetchall()
            for x in data_list:
                country_id = x[0]
                country_code = x[1]
                country_name = x[2]
                cont_id = x[3]
                wiki = x[4]
                kw = x[5]
                country = Country(country_id, country_code, country_name, cont_id, wiki,
                                  kw)
                yield p2app.events.CountrySearchResultEvent(country)
            connection.close()

        elif country_name is not None and country_code is not None:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM country WHERE name = ? AND country_code = ?",
                                 (country_name, country_code))
            data_list = var.fetchall()
            for x in data_list:
                country_id = x[0]
                country_code = x[1]
                country_name = x[2]
                cont_id = x[3]
                wiki = x[4]
                kw = x[5]
                country = Country(country_id, country_code, country_name, cont_id, wiki,
                                  kw)
                yield p2app.events.CountrySearchResultEvent(country)
            connection.close()

    def load_country_event(self): #need to fix this somehow
        """Function to load the data if shown in the database based on the country_ID"""
        country_ID = self.cont_obj.country_id()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        var = cursor.execute("SELECT * FROM country WHERE country_id = ?", (country_ID,))
        data_list = var.fetchall()
        for x in data_list:
            country_id = x[0]
            country_code = x[1]
            country_name = x[2]
            cont_id = x[3]
            wiki = x[4]
            kw = x[5]
            country = Country(country_id, country_code, country_name, cont_id, wiki,
                              kw)
            yield p2app.events.CountryLoadedEvent(country)
        connection.close()

    def save_new_country_event(self): #need to fix somehow
        """Function to save a new country if it fits the SQL criteria"""
        country_namedtuple = self.cont_obj._country
        country_id = country_namedtuple.country_id #will always be none
        country_code = country_namedtuple.country_code
        country_name = country_namedtuple.name
        cont_id = country_namedtuple.continent_id
        wiki_link = country_namedtuple.wikipedia_link
        keywords = country_namedtuple.keywords
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        try:
            cursor.execute(
                'INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?)',
                (country_id, country_code, country_name, cont_id, wiki_link, keywords))
            connection.commit()
            my_country = Country(country_id = country_id, country_code = country_code,
                                 name = country_name, continent_id = cont_id,
                                 wikipedia_link = wiki_link, keywords = keywords)
            yield p2app.events.CountrySavedEvent(my_country)
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            yield p2app.events.SaveCountryFailedEvent("There already exists an ID in the SQL Database, or you have inputted the wrong values")
        connection.close()

    def save_country_event(self):
        """Function to save a country after using the load data function to save new data of that region"""
        country_namedtuple = self.cont_obj._country
        country_id = country_namedtuple.country_id
        country_code = country_namedtuple.country_code
        country_name = country_namedtuple.name
        cont_id = country_namedtuple.continent_id
        wiki_link = country_namedtuple.wikipedia_link
        keywords = country_namedtuple.keywords
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute(
                'UPDATE country SET country_code=?, name=?, continent_id=?, wikipedia_link=?, keywords=? WHERE country_id=?',
                (country_code, country_name, cont_id, wiki_link, keywords, country_id))
            connection.commit()
            my_country = Country(country_id = country_id, country_code = country_code,
                                 name = country_name, continent_id = cont_id,
                                 wikipedia_link = wiki_link, keywords = keywords)
            yield p2app.events.CountrySavedEvent(my_country)
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            yield p2app.events.SaveCountryFailedEvent("There already exists an ID in the SQL Database, or you are inputting the wrong values")
        connection.close()