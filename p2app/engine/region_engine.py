import p2app.events
import sqlite3
from collections import namedtuple

Region = namedtuple(
    'Region',
    ['region_id', 'region_code', 'local_code', 'name',
     'continent_id', 'country_id', 'wikipedia_link', 'keywords'])

class Region_manager:
    """Class to have all my region data split up"""
    def __init__(self,cont_obj,db_path):
        """Initialize my data which I need to use"""
        self.cont_obj = cont_obj
        self.db_path = db_path

    def start_region_search_event(self): #works
        """Start the search for my region which yields back the necessary data depending on what you input in the GUI"""
        region_code = self.cont_obj.region_code()
        local_code = self.cont_obj.local_code()
        region_name = self.cont_obj.name()

        if region_name is None and region_code is not None and local_code is None:  # just the region code
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM region WHERE region_code = ?", (region_code,))
            data_list = var.fetchall()
            for x in data_list:
                r_id = x[0]
                r_code = x[1]
                l_code = x[2]
                r_name = x[3]
                cont_id = x[4]
                country_id = x[5]
                wiki_link = x[6]
                kw = x[7]
                region = Region(r_id, r_code, l_code, r_name, cont_id, country_id, wiki_link, kw)
                yield p2app.events.RegionSearchResultEvent(region)
            connection.close()
        elif region_name is not None and region_code is None and local_code is None:  # just the region name
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM region WHERE name = ?", (region_name,))
            data_list = var.fetchall()
            for x in data_list:
                r_id = x[0]
                r_code = x[1]
                l_code = x[2]
                r_name = x[3]
                cont_id = x[4]
                country_id = x[5]
                wiki_link = x[6]
                kw = x[7]
                region = Region(r_id, r_code, l_code, r_name, cont_id, country_id, wiki_link, kw)
                yield p2app.events.RegionSearchResultEvent(region)
            connection.close()
        elif region_name is not None and region_code is not None and local_code is None:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM region WHERE name = ? AND region_code = ?",
                                 (region_name, region_code))
            data_list = var.fetchall()
            for x in data_list:
                r_id = x[0]
                r_code = x[1]
                l_code = x[2]
                r_name = x[3]
                cont_id = x[4]
                country_id = x[5]
                wiki_link = x[6]
                kw = x[7]
                region = Region(r_id, r_code, l_code, r_name, cont_id, country_id, wiki_link, kw)
                yield p2app.events.RegionSearchResultEvent(region)
            connection.close()
        elif region_name is None and region_code is None and local_code is not None:  # just the local name
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM region WHERE local_code = ?", (local_code,))
            data_list = var.fetchall()
            for x in data_list:
                r_id = x[0]
                r_code = x[1]
                l_code = x[2]
                r_name = x[3]
                cont_id = x[4]
                country_id = x[5]
                wiki_link = x[6]
                kw = x[7]
                region = Region(r_id, r_code, l_code, r_name, cont_id, country_id, wiki_link, kw)
                yield p2app.events.RegionSearchResultEvent(region)
            connection.close()
        elif region_name is not None and region_code is None and local_code is not None:  # region name and local name
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM region WHERE name = ? AND local_code = ?",
                                 (region_name, local_code))
            data_list = var.fetchall()
            for x in data_list:
                r_id = x[0]
                r_code = x[1]
                l_code = x[2]
                r_name = x[3]
                cont_id = x[4]
                country_id = x[5]
                wiki_link = x[6]
                kw = x[7]
                region = Region(r_id, r_code, l_code, r_name, cont_id, country_id, wiki_link, kw)
                yield p2app.events.RegionSearchResultEvent(region)
            connection.close()
        elif region_name is None and region_code is not None and local_code is not None:  # region code and local name
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            var = cursor.execute("SELECT * FROM region WHERE region_code = ? AND local_code = ?",
                                 (region_code, local_code))
            data_list = var.fetchall()
            for x in data_list:
                r_id = x[0]
                r_code = x[1]
                l_code = x[2]
                r_name = x[3]
                cont_id = x[4]
                country_id = x[5]
                wiki_link = x[6]
                kw = x[7]
                region = Region(r_id, r_code, l_code, r_name, cont_id, country_id, wiki_link, kw)
                yield p2app.events.RegionSearchResultEvent(region)
            connection.close()
    def load_region_event(self):
        """Function to load the data if shown in the database based on the region_id"""
        region_id = self.cont_obj.region_id()
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        var = cursor.execute("SELECT * FROM region WHERE region_id = ?", (region_id,))
        data_list = var.fetchall()
        for x in data_list:
            r_id = x[0]
            r_code = x[1]
            l_code = x[2]
            r_name = x[3]
            cont_id = x[4]
            country_id = x[5]
            wiki_link = x[6]
            kw = x[7]
            region = Region(r_id, r_code, l_code, r_name, cont_id, country_id, wiki_link, kw)
            yield p2app.events.RegionLoadedEvent(region)
        connection.close()


    def save_new_region_event(self):
        """Function to save a new region if it fits the SQL criteria"""
        region_namedtuple = self.cont_obj._region
        region_id = region_namedtuple.region_id
        region_code = region_namedtuple.region_code
        local_code = region_namedtuple.local_code
        region_name = region_namedtuple.name
        cont_id = region_namedtuple.continent_id
        country_id = region_namedtuple.country_id
        wiki_link = region_namedtuple.wikipedia_link
        keywords = region_namedtuple.keywords

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        if region_code is None or cont_id is None or local_code is None or region_name is None or country_id is None:
            yield p2app.events.ErrorEvent("You cannot input null values")
        try:
            cursor.execute(
                'INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (region_id,region_code,local_code,region_name,cont_id,country_id,wiki_link,keywords))
            connection.commit()
            region = Region(region_id, region_code, local_code, region_name, cont_id, country_id, wiki_link, keywords)
            yield p2app.events.RegionSavedEvent(region)
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            yield p2app.events.SaveRegionFailedEvent("There already exists an ID in the SQL Database, or you are inputting the wrong values")
        connection.close()


    def save_region_event(self):
        """Function to save a region after using the load data function to save new data of that region"""
        region_namedtuple = self.cont_obj._region
        region_id = region_namedtuple.region_id
        region_code = region_namedtuple.region_code
        local_code = region_namedtuple.local_code
        region_name = region_namedtuple.name
        cont_id = region_namedtuple.continent_id
        country_id = region_namedtuple.country_id
        wiki_link = region_namedtuple.wikipedia_link
        keywords = region_namedtuple.keywords

        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute('PRAGMA foreign_keys = ON;')
            cursor.execute(
                'UPDATE region SET (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (region_id,region_code,local_code,region_name,cont_id,country_id,wiki_link,keywords))
            connection.commit()
            region = Region(region_id, region_code, local_code, region_name, cont_id, country_id,
                            wiki_link, keywords)
            yield p2app.events.RegionSavedEvent(region)
        except sqlite3.IntegrityError or sqlite3.OperationalError:
            yield p2app.events.SaveRegionFailedEvent("There already exists an ID in the SQL Database, or you are inputting the wrong values")
        connection.close()

