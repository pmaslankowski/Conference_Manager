# Conference Manager App
# Author: Piotr Maślankowski
# Databases, UWr, June 2017



test_event = '{"event":{"login": "test2", "password": "password2", "eventname": "Event2", "start_timestamp":"22-10-2015", "end_timestamp": "23-10-2015"}}'
test_user = '{"user": {"login": "test3", "password": "password3", "newlogin": "testuser", "newpassword": "testuser"}}'
test_talk = '{"talk": {"login": "test3", "password": "password3", "speakerlogin": "test1", "talk": "talk4", "title": "Talk4Title", "start_timestamp": "15-05-2017", "room": 120, "initial_evaluation": 5, "eventname": "Event1"}}'
test_register_user_for_event = '{"register_user_for_event": {"login": "test2", "password": "password2", "eventname": "Event1"}}'
test_attendance = '{"attendance": {"login": "test1", "password": "password1", "talk": "talk1"}}'
test_evaluation = '{"evaluation": {"login": "test3", "password": "password3", "talk": "talk4", "rating": 10}}'
test_reject = '{"reject": {"login": "test3", "password": "password3", "talk": "talk1"}}'
test_reject2 = '{"reject": {"login": "test3", "password": "password3", "talk": "talk4"}}'
test_proposal = '{"proposal": {"login": "test2", "password": "password2", "talk": "talk_proposition", "title": "wild title", "start_timestamp": "16-05-2017 15:00", "eventname": "Event1"}}'
test_talk2 = '{"talk": {"login": "test3", "password": "password3", "speakerlogin": "test1", "talk": "talk_proposition", "title": "Wild Title 2", "start_timestamp": "20-05-2017", "room": 130, "initial_evaluation": 4, "eventname": "Event1"}}'
test_friends = '{"friends": {"login1": "test1", "password": "password1", "login2": "test3"}}'
test_user_plan = '{"user_plan": {"login": "test1", "limit": 0}}'
test_user_plan2 = '{"user_plan": {"login": "test1", "limit": 1}}'
test_day_plan = '{"day_plan": {"timestamp": "19-07-2017 15:00"}}'
test_best_talks = '{"best_talks": {"start_timestamp": "10-07-2017", "end_timestamp": "21-07-2017", "all": 1, "limit": 0}}'
test_best_talks2 = '{"best_talks": {"start_timestamp": "10-07-2017", "end_timestamp": "21-07-2017", "all": 0, "limit": 1}}'
test_most_popular_talks = '{"most_popular_talks": {"start_timestamp": "10-07-2017", "end_timestamp": "21-07-2017", "limit": 0}}'
test_attended_talks = '{"attended_talks": {"login": "test1", "password": "password1"}}'
test_abandoned_talks = '{"abandoned_talks": {"login": "test3", "password": "password3", "limit": 0}}'
test_recently_added_talks = '{"recently_added_talks": {"limit": 2}}'
test_proposals = '{"proposals": {"login": "test3", "password": "password3"}}'
test_friends_talks = '{"friends_talks": {"login": "test1", "password": "password1", "start_timestamp": "10-07-2017", "end_timestamp": "21-07-2017", "limit": 5}}'
test_friends_events = '{"friends_events": {"login": "test1", "password": "password1"}}'
test_recommended_talks = '{"recommended_talks": {"login": "test1", "password": "password1", "start_timestamp": "10-07-2017", "end_timestamp": "21-07-2017", "limit": 5}}'
