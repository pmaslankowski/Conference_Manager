# Conference Manager App
# Author: Piotr Maślankowski
# Databases, UWr, June 2017


import psycopg2


class Database(object):
    """
    Database manager class.
    Manages connection to database, performing queries etc.
    Available methods:
        - open(dbname, username, password) -- open connection to database
        - close() -- close connection
        - execute(query) -- execute query (results are stored in query object as side effect)
        - check_tables() -- check if actual tables exists in database. Returns boolean
    """
    _conn = None
    _cursor = None
    opened = False


    def __init__(self, logging=False):
        self._logging = logging


    def open(self, dbname, username, password):
        """Open connection to database"""
        try:
            self._conn = psycopg2.connect(dbname=dbname,
                                          user=username,
                                          password=password,
                                          host='localhost')
            self._cursor = self._conn.cursor()
            print(r'{"status": "OK"}')
            self.opened = True

            if self._logging:
                print('Connection to database established.')

        except (Exception, psycopg2.DatabaseError) as error:
            print(r'{"status": "ERROR", "desc": "Wrong database login data"}')


    def close(self):
        """Close connection to database"""
        self.opened = False
        if self._conn is not None:
            self._conn.close()
            if self._logging:
                print('Connection closed.')


    def create_tables(self):
        try:
            self._cursor.execute(open('create_database.sql', 'r').read())
        except:
            self._conn.rollback()


    def check_authentication(self, login, password, expected_level):
        sql_query = "SELECT check_user('{}','{}')".format(login, password)
        self._cursor.execute(sql_query)
        real_auth_level, = self._cursor.fetchone()
        return real_auth_level == expected_level or (real_auth_level == 'organiser' and expected_level == 'participant')


    def execute(self, query):
        try:
            if query.name == 'organizer':
                if query.auth_data != 'd8578edf8458ce06fbc5bb76a58c5ca4':
                    query.status = 'ERROR'
                    if self._logging:
                        print('Failed authentication - wrong secret.')
                else:
                    query.auth_data = None

            if query.auth_data is not None and not self.check_authentication(*query.auth_data):
                query.status = 'ERROR'
                if self._logging:
                    print('Failed authentication')
            else:
                self._cursor.execute(query.sql, query.placeholders)
                if(not(query.modifying)):
                    query.raw_result = self._cursor.fetchall()
                self._conn.commit()
                query.executed = True
                query.status = 'OK'

                if self._logging:
                        print('Query was sucessfully executed')
                        if(not(query.modifying)):
                            print('(returning {} row(s))'.format(len(query.raw_result)))
        except (psycopg2.InternalError, psycopg2.IntegrityError,
                psycopg2.DataError, psycopg2.ProgrammingError) as err:
            query.status = 'ERROR'
            query.desc = str(err).replace('\n', ' ').replace('"', "'")
            self._conn.rollback()
                #print('ERROR:'+query.name)
