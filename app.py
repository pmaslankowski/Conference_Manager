# Conference Manager App
# Author: Piotr Maślankowski
# Databases, UWr, June 2017

import sys
from database import Database
from query import Query
from query_builder import QueryBuilder
from unit_tests import *

builder = QueryBuilder()
q1 = builder.build_query(test_event)
q2 = builder.build_query(test_user)
q3 = builder.build_query(test_talk)
q4 = builder.build_query(test_register_user_for_event)
q5 = builder.build_query(test_attendance)
q6 = builder.build_query(test_evaluation)
q7 = builder.build_query(test_reject)
q8 = builder.build_query(test_reject2)
q9 = builder.build_query(test_proposal)
q10 = builder.build_query(test_talk2)
q11 = builder.build_query(test_friends)

db = Database(True)
db.open('conference_database', 'app_api', '123456')
db.execute(q11)
q11.parse_result()
print(q11.result)
db.close()
