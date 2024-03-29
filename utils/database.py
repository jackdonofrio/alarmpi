"""
Module for creating and managing sqlite3 databases
** Currently deprecated **
"""

import os
import sqlite3

class Column:
    """ Class for handling column data between Python and SQLite """
    def __init__(self, name, item_type, value=None):
        self.name = name
        self.type = item_type
        self.value = f'"{value}"' if item_type == 'TEXT' else value

class Database:
    """ Class for storing and managing data for clock modules """
    PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')
    def __init__(self):
        self.connection = sqlite3.connect(self.PATH)
        self.cursor = self.connection.cursor()

    def create_new_table(self, table_name, columns):
        """ Creates a new table, given its name is not taken """
        command = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        command += ', '.join([f'{column.name} {column.type}' for column in columns]) + ')'
        self.cursor.execute(command)
        self.connection.commit()

    def add_to_table(self, table_name, columns):
        """ Adds new row of column values to table """
        command = f'INSERT INTO {table_name} ('
        command += ', '.join([f'{column.name}' for column in columns]) + ') VALUES ('
        command += ', '.join([f'{column.value}' for column in columns]) + ')'
        self.cursor.execute(command)
        self.connection.commit()

    @staticmethod
    def sanitize_value(value_type, value):
        """ Converts Python strings to SQLite strings if necessary """

        return f'"{value}"' if value_type == 'TEXT' else value

    def update_value(self, table_name, column, new_value):
        """ Updates value in a column of an existing row """
        command = f"UPDATE {table_name} SET {column.name} = " + \
            f"{self.sanitize_value(column.type, new_value)} " + \
            f"WHERE {column.name} = {column.value}"
        self.cursor.execute(command)
        self.connection.commit()

    def get_value_from_table(self, table_name, column_name, expected_value=None):
        """ Retrieves value from column(s) within table row(s) """
        command = f"SELECT {column_name} FROM {table_name}"
        if expected_value:
            command += "WHERE {column_name} = {expected_value}"
        return self.cursor.execute(command).fetchall()

    def get_table_size(self, table_name):
        """ Returns the number of rows existing in the table """
        command = f"SELECT * FROM {table_name}"
        return len(self.cursor.execute(command).fetchall())

    def close_connection(self):
        """ Closes database connection """
        self.connection.close()
