-- Test trigger on invitation_friend_of
INSERT INTO conf_user(id, password) VALUES('test1', 'password1');
INSERT INTO conf_user(id, password) VALUES('test2', 'password2');
INSERT INTO conf_user(id, password, usertype) VALUES ('test3', 'password3', 'organiser');

-- case 1:
INSERT INTO invitation_friend_of VALUES('test1', 'test2');
INSERT INTO invitation_friend_of VALUES('test2', 'test1');
INSERT INTO invitation_friend_of VALUES('test1', 'test3');
INSERT INTO invitation_friend_of VALUES('test3', 'test1');
-- case 2:
INSERT INTO invitation_friend_of VALUES('test2', 'test1');

-- case 3:
INSERT INTO event(id, start_date, finish_date)
VALUES ('Event1', '10-07-2017', '20-07-2017');
INSERT INTO talk(id, userid, eventid, title, start_timestamp, status, room)
VALUES('talk1', 'test1', 'Event1', 'TalkTitle1', '15-07-2017 8:00', 'accepted', 1);
INSERT INTO talk(id, userid, eventid, title, start_timestamp, status, room)
VALUES('talk2', 'test2', 'Event1', 'TalkTitle2', '19-07-2017 8:00', 'accepted', 2);
INSERT INTO talk(id, userid, eventid, title, start_timestamp, status, room)
VALUES('talk3', 'test2', 'Event1', 'TalkTitle3', '19-07-2017 12:00', 'accepted', 2);
INSERT INTO talk(id, userid, eventid, title, start_timestamp, status, room)
VALUES('talk4', 'test1', 'Event1', 'TalkTitle4', '19-07-2017 7:00', 'accepted', 1);
INSERT INTO talk(id, userid, eventid, title, start_timestamp)
VALUES('talk5', 'test1', 'Event1', 'TalkTitle5', '16-07-2017 7:00');

INSERT INTO user_registered_at_event(userid, eventid) VALUES('test1', 'Event1');
INSERT INTO user_registered_at_event(userid, eventid) VALUES('test2', 'Event1');
INSERT INTO user_registered_at_event(userid, eventid) VALUES('test3', 'Event1');

INSERT INTO user_talk_rating VALUES('test1', 'talk1', 10);
INSERT INTO user_talk_rating VALUES('test2', 'talk1', 5);
INSERT INTO user_talk_rating VALUES('test3', 'talk1', 2);
INSERT INTO user_talk_rating VALUES('test1', 'talk2', 1);
INSERT INTO user_talk_rating VALUES('test2', 'talk2', 10);
INSERT INTO user_talk_rating VALUES('test3', 'talk2', 10);
INSERT INTO user_talk_rating VALUES('test1', 'talk3', 10);
INSERT INTO user_talk_rating VALUES('test2', 'talk3', 10);
INSERT INTO user_present_at_talk VALUES('test1', 'talk1');
INSERT INTO user_present_at_talk VALUES('test3', 'talk1');
INSERT INTO user_present_at_talk VALUES('test1', 'talk2');
-- case 4:
SELECT create_user('nowy_user', '123456');
