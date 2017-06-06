# Conference Manager App
# Author: Piotr Maślankowski
# Databases, UWr, June 2017

import sys, json
from database import Database
from query import Query

class QueryBuilder:
    def build_query(self, json_object):
        command = json.loads(json_object)
        cmd_name = list(command.keys())[0]

        try:
            build_query = getattr(self, cmd_name)
        except AttributeError:
            raise NotImplementedError('Function {} is not implemented'.format(cmd_name))

        arguments = command[cmd_name]
        query_data = build_query(cmd_name, arguments)
        return Query(*query_data)


    def event(self, name, args):
        columns = []
        query = 'INSERT INTO event(name, start_date, finish_date) VALUES(%s, %s, %s)'
        placeholders = [args['eventname'], args['start_timestamp'], args['end_timestamp']]
        auth_data = (args['login'], args['password'], 'organiser')
        return name, columns, query, placeholders, True, auth_data



builder = QueryBuilder()
q = builder.build_query('{"event":{"login": "test2", "password": "password2", "eventname": "name1", "start_timestamp":"22-10-2015", "end_timestamp": "23-10-2015"}}')
print(q)

db = Database(True)
db.open('conference_database', 'app_api', '123456')
db.execute(q)
q.parse_result()
print(q.result)
db.close()

#query1 = Query(['id','name', 'start_date', 'finish_date'],
#               'SELECT id, name, start_date, finish_date FROM event',
#               None)

#db.execute(query1)
#query1.parse_result()
# print(query1.result)
# db.close()
