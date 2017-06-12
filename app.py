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
q12 = builder.build_query(test_user_plan)
q13 = builder.build_query(test_user_plan2)
q14 = builder.build_query(test_day_plan)
q15 = builder.build_query(test_best_talks)
q16 = builder.build_query(test_best_talks2)
q17 = builder.build_query(test_most_popular_talks)
q18 = builder.build_query(test_attended_talks)
q19 = builder.build_query(test_abandoned_talks)
q20 = builder.build_query(test_recently_added_talks)
q21 = builder.build_query(test_proposals)
q22 = builder.build_query(test_friends_talks)
q23 = builder.build_query(test_friends_events)
q24 = builder.build_query(test_recommended_talks)

db = Database(True)
db.open('conference_database', 'app_api', '123456')
db.execute(q24)
q24.parse_result()
print(q24.result)
db.close()
