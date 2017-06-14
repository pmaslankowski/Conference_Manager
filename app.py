# Conference Manager App
# Author: Piotr Maślankowski
# Databases, UWr, June 2017

import sys
import json
from database import Database
from query import Query
from query_builder import QueryBuilder

db = Database(False)
openline = sys.stdin.readline()
opendict = json.loads(openline)['open']
db.open(opendict['baza'], opendict['login'], opendict['password'])

if db.opened:
    db.create_tables()

    builder = QueryBuilder()

    for line in sys.stdin:
        try:
            query = builder.build_query(line)
            db.execute(query)
            query.parse_result()
            print(query.result)
        except NotImplementedError:
            print(r'{"status": "NOT IMPLEMENTED"}')
    db.close()
