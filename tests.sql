-- Test trigger on invitation_friend_of
INSERT INTO conf_user(login, password) VALUES('test1', 'password1');
INSERT INTO conf_user(login, password) VALUES('test2', 'password2');
INSERT INTO conf_user(login, password, usertype) VALUES ('test3', 'password3', 'organiser');

-- case 1:
INSERT INTO invitation_friend_of VALUES(1, 2);
INSERT INTO invitation_friend_of VALUES(2, 1);

-- case 2:
INSERT INTO invitation_friend_of VALUES(2, 1);

-- case 3:
INSERT INTO event(name, start_date, finish_date)
VALUES ('Event1', '10-05-2017', '20-05-2017');
INSERT INTO talk(userid, eventid, title, start_timestamp)
VALUES(1, 1, 'talk1', '15-05-2017 8:00');
INSERT INTO talk(userid, eventid, title, start_timestamp)
VALUES(2, 1, 'talk2', '22-05-2017 8:00');
