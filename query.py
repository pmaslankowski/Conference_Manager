# Conference Manager App
# Author: Piotr Maślankowski
# Databases, UWr, June 2017

import json
from datetime import date, datetime


class Query(object):
    """Wrapper class for queries."""

    sql = None            # sql query
    placeholders = None   # list with placeholders fills
    columns = None        # table column names
    raw_result = None
    result = None         # json result string
    executed = False      # flag is true if query was executed
    modifying = False     # flag is true if query is modyfing database
    name = None
    status = 'ERROR'
    auth_data = None      # tuple consisting login, password
                          # and expected priviliges level


    def __init__(self, name, columns, sql, placeholders, modifying, auth_data):
        """ Keyword arguments:
            name -- name of query
            columns -- list with column names in query
            sql     -- sql query string
            placeholders -- data to fill placeholders in query
            modifying -- true if query only modify database"""

        self.name = name
        self.columns = columns
        self.sql = sql
        self.placeholders = placeholders
        self.modifying = modifying
        self.auth_data = auth_data
        self.desc = ''


    def __str__(self):
        return 'Query: {}\nColumns: {}\nSQL: {}\nPlaceholders: {}\n'.format(
            self.name, self.columns, self.sql, self.placeholders)


    def parse_result(self):
        """Parse result to json string. This string is ready to be printed.
           Result is stored in self.result"""

        def parse_one_record(record):
            return {col : str(val) for col, val in zip(self.columns, record)}

        def auxilary_date_serializer(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat(' ')
            raise TypeError ("Type {} is not serializable".format(type(obj)))


        if self.status == 'ERROR':
            self.result = '{"status": "ERROR", "desc": "' + str(self.desc) + '"}'
        elif self.modifying:
            self.result = '{"status": "OK"}'
        else:
            parsed_records = [parse_one_record(record) for record in self.raw_result]
            json_dict = { 'status': 'OK', 'data': parsed_records}
            self.result = json.dumps(json_dict, default=auxilary_date_serializer)
