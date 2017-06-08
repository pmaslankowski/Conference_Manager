-- Test trigger on invitation_friend_of
INSERT INTO conf_user(id, password) VALUES('test1', 'password1');
INSERT INTO conf_user(id, password) VALUES('test2', 'password2');
INSERT INTO conf_user(id, password, usertype) VALUES ('test3', 'password3', 'organiser');

-- case 1:
INSERT INTO invitation_friend_of VALUES('test1', 'test2');
INSERT INTO invitation_friend_of VALUES('test2', 'test1');

-- case 2:
INSERT INTO invitation_friend_of VALUES('test2', 'test1');

-- case 3:
INSERT INTO event(id, start_date, finish_date)
VALUES ('Event1', '10-05-2017', '20-05-2017');
INSERT INTO talk(id, userid, eventid, title, start_timestamp)
VALUES('talk1', 'test1', 'Event1', 'TalkTitle1', '15-05-2017 8:00');
INSERT INTO talk(id, userid, eventid, title, start_timestamp)
VALUES('talk2', 'test2', 'Event1', 'TalkTitle2', '22-05-2017 8:00');

-- case 4:
SELECT create_user('nowy_user', '123456');
