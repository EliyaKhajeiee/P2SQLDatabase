#this is a class I am going to be doing all my continent stuff in

import p2app.events
import sqlite3
from collections import namedtuple

Continent = namedtuple('Continent', ['continent_id', 'continent_code', 'name'])

class Continent_manager:
    """Class to have all my continent data split up"""
    def __init__(self,cont_obj,db_path):
        """Initialize my data which I need to use"""
        self.cont_obj = cont_obj #Sent by view  : StartContinentSearchEvent: continent_code = 'EK', name = 'EliyaKhajeie'
        self.db_path = db_path

    def start_continent_search_event(self):
        """Start the search for my continent which yields back the necessary data depending on what you input in the GUI"""
        continent_code = self.cont_obj.continent_code()
        cont_name = self.cont_obj.name()

        if cont_name is None and continent_code is not None:  # just the cont code
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM continent WHERE continent_code = ?", (continent_code,))
            data_list = var.fetchall()
            for x in data_list:
                ID = x[0]
                code = x[1]
                continent = x[2]
                new_cont = Continent(continent_id = int(ID), continent_code = str(code),
                                     name = str(continent))
                yield p2app.events.ContinentSearchResultEvent(new_cont)
            connection.close()

        elif cont_name is not None and continent_code is None:  # just the cont_name
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM continent WHERE name = ?", (cont_name,))
            data_list = var.fetchall()
            for x in data_list:
                ID = x[0]
                code = x[1]
                continent = x[2]
                new_cont = Continent(continent_id = int(ID), continent_code = str(code),
                                     name = str(continent))
                yield p2app.events.ContinentSearchResultEvent(new_cont)
            connection.close()

        elif cont_name is not None and continent_code is not None:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM continent WHERE name = ? AND continent_code = ?", (cont_name, continent_code))
            data_list = var.fetchall()
            for x in data_list:
                ID = x[0]
                code = x[1]
                continent = x[2]
                new_cont = Continent(continent_id = int(ID), continent_code = str(code),
                                     name = str(continent))
                yield p2app.events.ContinentSearchResultEvent(new_cont)
            connection.close()

    def load_continent_event(self):
        """Function to load the data if shown in the database based on the continent_id"""
        cont_id = (self.cont_obj.continent_id())
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        var = cursor.execute("SELECT * FROM continent WHERE continent_id = ?", (cont_id,))
        data_list = var.fetchall()
        for x in data_list:
            ID = x[0]
            code = x[1]
            continent = x[2]
            new_cont = Continent(continent_id = int(ID), continent_code = str(code),
                                 name = str(continent))
            yield p2app.events.ContinentLoadedEvent(new_cont)
        connection.close()

    def save_new_continent_event(self):
        """Function to save a new continent if it fits the SQL criteria"""
        cont_namedtuple = self.cont_obj._continent
        cont_id = cont_namedtuple.continent_id
        continent_code = cont_namedtuple.continent_code
        cont_name = cont_namedtuple.name
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        if continent_code is None or cont_name is None:
            yield p2app.events.ErrorEvent("You cannot input null values")
        try:
            cursor.execute('INSERT INTO continent (continent_id, continent_code, name) VALUES (?, ?, ?)',
                           (cont_id, continent_code, cont_name))
            connection.commit()
            new_cont = Continent(continent_id = cont_id, continent_code = str(continent_code),
                                 name = str(cont_name))
            yield p2app.events.ContinentSavedEvent(new_cont)
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            yield p2app.events.SaveContinentFailedEvent("There already exists an ID in the SQL Database")
        connection.close()

    def save_continent_event(self):
        """Function to save a continent after using the load data function to save new data of that region"""
        cont_namedtuple = self.cont_obj._continent
        cont_id = cont_namedtuple.continent_id
        continent_code = cont_namedtuple.continent_code
        cont_name = cont_namedtuple.name
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        if continent_code is None or cont_name is None:
            yield p2app.events.ErrorEvent("You cannot input null values")
        try:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute('UPDATE continent SET continent_code = ?, name = ? WHERE continent_id = ?',
                (continent_code, cont_name, cont_id))
            connection.commit()
            new_cont = Continent(continent_id = cont_id, continent_code = str(continent_code),
                                 name = str(cont_name))
            yield p2app.events.ContinentSavedEvent(new_cont)
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            yield p2app.events.SaveContinentFailedEvent("There already exists an ID in the SQL Database, or you are inputting the wrong values ")
        connection.close()













