-- Tworzenie bazy danych dla konferencji
-- naukowej
-- Autor: Piotr Maślankowski
-- Maj 2017


-- create  domains:
CREATE DOMAIN TalkStatus AS text
	CHECK(VALUE IN ('accepted', 'rejected', 'awaiting')) NOT NULL;

CREATE DOMAIN TalkRating AS integer
	CHECK(VALUE IN (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)) NOT NULL;

CREATE DOMAIN UserType AS text
	CHECK(VALUE IN ('organiser', 'participant')) NOT NULL;


-- create tables:
CREATE TABLE event(
	id VARCHAR(255) PRIMARY KEY,
	start_date date NOT NULL,
	finish_date date NOT NULL,
  CONSTRAINT valid_dates CHECK (start_date <= finish_date));

CREATE TABLE talk(
	id text PRIMARY KEY,
	userid varchar(50) NOT NULL,
	eventid varchar(255),
	status TalkStatus DEFAULT 'awaiting',
	title text NOT NULL,
	room integer CHECK(room >= 0),
	start_timestamp timestamp,
	registration_timestamp timestamp DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE conf_user(
	id varchar(50) PRIMARY KEY,
	password varchar(50) NOT NULL,
	usertype UserType DEFAULT 'participant');

CREATE TABLE user_registered_at_event(
	userid varchar(50) NOT NULL,
	eventid varchar(255) NOT NULL,
  PRIMARY KEY(userid, eventid));

CREATE TABLE user_talk_rating(
	userid varchar(50) NOT NULL,
	talkid text NOT NULL,
	rating TalkRating DEFAULT 0,
  PRIMARY KEY(userid, talkid));

CREATE TABLE user_present_at_talk(
	userid varchar(50) NOT NULL,
	talkid text NOT NULL,
  PRIMARY KEY(userid, talkid));

CREATE TABLE invitation_friend_of(
	userid1 varchar(50) NOT NULL,
	userid2 varchar(50) NOT NULL,
  PRIMARY KEY(userid1, userid2));

CREATE TABLE friend_of(
	userid1 varchar(50) NOT NULL,
	userid2 varchar(50) NOT NULL,
	PRIMARY KEY(userid1, userid2),
  CONSTRAINT id_order CHECK(userid1 < userid2));


-- foreign key constraints:
ALTER TABLE talk
  ADD CONSTRAINT fk_talk_user
  FOREIGN KEY (userid) REFERENCES conf_user(id) DEFERRABLE;
ALTER TABLE talk
  ADD CONSTRAINT fk_talk_event
  FOREIGN KEY (eventid) REFERENCES event(id) DEFERRABLE;

ALTER TABLE user_registered_at_event
  ADD CONSTRAINT fk_user_registered_at_event_user
  FOREIGN KEY (userid) REFERENCES conf_user(id) DEFERRABLE;
ALTER TABLE user_registered_at_event
  ADD CONSTRAINT fk_user_registered_at_event_event
	FOREIGN KEY (eventid) REFERENCES event(id) DEFERRABLE;

ALTER TABLE user_talk_rating
  ADD CONSTRAINT fk_user_talk_rating_user
	FOREIGN KEY (userid) REFERENCES conf_user(id) DEFERRABLE;
ALTER TABLE user_talk_rating
  ADD CONSTRAINT fk_user_talk_rating_talk
	FOREIGN KEY (talkid) REFERENCES talk(id) DEFERRABLE;

ALTER TABLE user_present_at_talk
  ADD CONSTRAINT fk_user_present_at_talk_user
	FOREIGN KEY (userid) REFERENCES conf_user(id) DEFERRABLE;
ALTER TABLE user_present_at_talk
  ADD CONSTRAINT fk_user_present_at_talk_talk
	FOREIGN KEY (talkid) REFERENCES talk(id) DEFERRABLE;

ALTER TABLE invitation_friend_of
  ADD CONSTRAINT fk_invitation_friend_of_friend1
	FOREIGN KEY (userid1) REFERENCES conf_user(id) DEFERRABLE;
ALTER TABLE invitation_friend_of
  ADD CONSTRAINT fk_invitation_friend_of_friend2
	FOREIGN KEY (userid2) REFERENCES conf_user(id) DEFERRABLE;

ALTER TABLE friend_of
  ADD CONSTRAINT fk_friend_of_friend1
	FOREIGN KEY (userid1) REFERENCES conf_user(id) DEFERRABLE;
ALTER TABLE friend_of
  ADD CONSTRAINT fk_friend_of_friend2
	FOREIGN KEY (userid2) REFERENCES conf_user(id) DEFERRABLE;


--triggers:
CREATE OR REPLACE FUNCTION talk_timestamp_trigger()
RETURNS TRIGGER AS $X$
BEGIN
  NEW.registration_timestamp = now();
	RETURN NEW;
END;
$X$ LANGUAGE plpgsql;

CREATE TRIGGER on_insert_to_talk BEFORE INSERT ON talk
FOR EACH ROW EXECUTE PROCEDURE talk_timestamp_trigger();
CREATE TRIGGER on_update_to_talk BEFORE UPDATE ON talk
FOR EACH ROW EXECUTE PROCEDURE talk_timestamp_trigger();


CREATE OR REPLACE FUNCTION invitation_friend_of_trigger()
RETURNS TRIGGER AS $X$
DECLARE
  lower_id varchar(50);
	higher_id varchar(50);
BEGIN
	IF NEW.userid1 < NEW.userid2 THEN
		lower_id := NEW.userid1;
		higher_id := NEW.userid2;
	ELSE
	  lower_id := NEW.userid2;
		higher_id := NEW.userid1;
	END IF;

	-- check if users are already friends:
	IF EXISTS (
		SELECT * FROM friend_of
		WHERE userid1=lower_id AND userid2=higher_id)
	THEN
		DELETE FROM invitation_friend_of
		WHERE userid1=NEW.userid1 AND userid2=NEW.userid2;
	END IF;

  IF EXISTS (
		SELECT * FROM invitation_friend_of
		WHERE userid1=NEW.userid2 AND userid2=NEW.userid1)
	THEN
	  INSERT INTO friend_of VALUES (lower_id, higher_id);
		DELETE FROM invitation_friend_of
		WHERE userid1=NEW.userid2 AND userid2=NEW.userid1;
		DELETE FROM invitation_friend_of
		WHERE userid1=NEW.userid1 AND userid2=NEW.userid2;
	END IF;

	RETURN NEW;
END;
$X$ LANGUAGE plpgsql;

CREATE TRIGGER on_insert_to_invitation_friend_of
AFTER INSERT ON invitation_friend_of
FOR EACH ROW EXECUTE PROCEDURE invitation_friend_of_trigger();


CREATE OR REPLACE FUNCTION talk_trigger()
RETURNS TRIGGER AS $X$
DECLARE
	event_start_date date;
	event_finish_date date;
BEGIN
	IF (NEW.id, 'accepted') IN (SELECT id, status FROM talk) OR
	   (NEW.id, 'rejected') IN (SELECT id, status FROM talk) THEN
		RAISE EXCEPTION 'Talk already exists';
		RETURN NULL;
	END IF;

	SELECT start_date INTO event_start_date FROM event
	WHERE id = NEW.eventid;
	SELECT finish_date INTO event_finish_date FROM event
	WHERE id = NEW.eventid;
	IF NEW.start_timestamp::DATE BETWEEN event_start_date AND event_finish_date THEN
	 	RETURN NEW;
	ELSE
		RAISE EXCEPTION 'Wrong start_timestamp for talk: %', NEW.id;
		RETURN NULL;
	END IF;
END;
$X$ LANGUAGE plpgsql;

CREATE TRIGGER on_insert_to_talk_check_timestamp
BEFORE INSERT ON talk
FOR EACH ROW EXECUTE PROCEDURE talk_trigger();


CREATE OR REPLACE FUNCTION create_user(username VARCHAR(50), pass VARCHAR(50))
RETURNS void AS $X$
BEGIN
	INSERT INTO conf_user(id, password) VALUES(username, pass);
END;
$X$ LANGUAGE plpgsql
SECURITY DEFINER;



CREATE OR REPLACE FUNCTION create_organiser(username VARCHAR(50), pass VARCHAR(50))
RETURNS void AS $X$
BEGIN
	INSERT INTO conf_user(id, password, usertype) VALUES(username, pass, 'organiser');
END;
$X$ LANGUAGE plpgsql
SECURITY DEFINER;


CREATE OR REPLACE FUNCTION check_user(username VARCHAR(50), pass VARCHAR(50))
RETURNS TEXT AS $X$
DECLARE
	real_pass VARCHAR(50);
BEGIN
	SELECT password INTO real_pass FROM conf_user
	WHERE id=username;
	IF real_pass = pass THEN
		RETURN (SELECT usertype FROM conf_user WHERE id=username);
	ELSE
		RETURN 'WRONG DATA';
	END IF;
END;
$X$ LANGUAGE plpgsql
SECURITY DEFINER;

DROP FUNCTION rejected_talks(username VARCHAR(50), pass VARCHAR(50));
CREATE OR REPLACE FUNCTION rejected_talks(username VARCHAR(50), pass VARCHAR(50))
RETURNS TABLE(talk text, speakerlogin varchar(50), start_timestamp_res timestamp, title_res text)
AS $X$
DECLARE
	usertype text;
BEGIN
	SELECT check_user(username, pass) INTO usertype;
	IF usertype = 'organiser' THEN
		RETURN QUERY SELECT id, userid, start_timestamp, title
		             FROM talk WHERE status = 'rejected';
	ELSE
		RETURN QUERY SELECT id, userid, start_timestamp, title
						     FROM talk WHERE status = 'rejected' AND userid = username;
	END IF;
END;
$X$ LANGUAGE plpgsql;


INSERT INTO event VALUES('', '01-01-0001', '01-01-9999');
