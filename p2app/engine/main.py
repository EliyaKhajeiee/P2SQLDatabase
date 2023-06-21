# p2app/engine/main.py
#
# ICS 33 Spring 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

import p2app.views.events
import p2app.events.database
import sqlite3
import p2app.engine.continent_engine,p2app.engine.country_engine,p2app.engine.region_engine

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.event_bus = p2app.events.EventBus()
        self.event_bus.register_engine(self)
        self.db_path = None

    def start(self,event):
        """My starting function which checks to see if the database is valid"""
        self.db_path = (event.path())
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]
            if 'country' not in tables or 'region' not in tables or 'continent' not in tables:
                yield p2app.events.database.DatabaseOpenFailedEvent("This is not a valid database")
                connection.close()
                return
        except sqlite3.DatabaseError:
            yield p2app.events.database.DatabaseOpenFailedEvent("This is not a valid database")
            connection.close()
            return
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')
            yield p2app.events.database.DatabaseOpenedEvent(self.db_path)
        except Exception as e:
            yield p2app.events.database.DatabaseOpenFailedEvent(str(e))

    def exit(self,event):
        """Event that yields exit application"""
        yield p2app.events.EndApplicationEvent()

    def close_database(self,event):
        """Event that is yielded when database is closed"""
        yield p2app.events.DatabaseClosedEvent()


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if isinstance(event,p2app.events.OpenDatabaseEvent):
            yield from self.start(event)
        if isinstance(event,p2app.events.QuitInitiatedEvent):
            yield from self.exit(event)
        if isinstance(event,p2app.events.CloseDatabaseEvent):
            yield from self.close_database(event)

        if isinstance(event,p2app.events.StartContinentSearchEvent):
            boo = p2app.engine.continent_engine.Continent_manager(event,self.db_path)
            yield from boo.start_continent_search_event()
        if isinstance(event,p2app.events.LoadContinentEvent):
            boo = p2app.engine.continent_engine.Continent_manager(event,self.db_path)
            yield from boo.load_continent_event()
        if isinstance(event,p2app.events.SaveNewContinentEvent):
            boo = p2app.engine.continent_engine.Continent_manager(event, self.db_path)
            yield from boo.save_new_continent_event()
        if isinstance(event,p2app.events.SaveContinentEvent):
            boo = p2app.engine.continent_engine.Continent_manager(event, self.db_path)
            yield from boo.save_continent_event()

        if isinstance(event,p2app.events.StartCountrySearchEvent):
            boo = p2app.engine.country_engine.Country_manager(event,self.db_path)
            yield from boo.start_country_search_event()
        if isinstance(event,p2app.events.LoadCountryEvent):
            boo = p2app.engine.country_engine.Country_manager(event,self.db_path)
            yield from boo.load_country_event()
        if isinstance(event,p2app.events.SaveNewCountryEvent):
            boo = p2app.engine.country_engine.Country_manager(event,self.db_path)
            yield from boo.save_new_country_event()
        if isinstance(event,p2app.events.SaveCountryEvent):
            boo = p2app.engine.country_engine.Country_manager(event,self.db_path)
            yield from boo.save_country_event()

        if isinstance(event,p2app.events.StartRegionSearchEvent):
            boo = p2app.engine.region_engine.Region_manager(event,self.db_path)
            yield from boo.start_region_search_event()
        if isinstance(event,p2app.events.LoadRegionEvent):
            boo = p2app.engine.region_engine.Region_manager(event,self.db_path)
            yield from boo.load_region_event()
        if isinstance(event,p2app.events.SaveNewRegionEvent):
            boo = p2app.engine.region_engine.Region_manager(event,self.db_path)
            yield from boo.save_new_region_event()
        if isinstance(event,p2app.events.SaveRegionEvent):
            boo = p2app.engine.region_engine.Region_manager(event,self.db_path)
            yield from boo.save_region_event()



        # This is a way to write a generator function that always yields zero values.
        # You'll want to remove this and replace it with your own code, once you start
        # writing your engine, but this at least allows the program to run.


