# Conference Manager App
# Author: Piotr Maślankowski
# Databases, UWr, June 2017


import json
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


    # query builders:
    # queries modifying database
    def event(self, name, args):
        """
        (*O) event <login> <password> <eventname> <start_timestamp> <end_timestamp>
        """
        columns = []
        query = 'INSERT INTO event(name, start_date, finish_date) VALUES(%s, %s, %s)'
        placeholders = [args['eventname'], args['start_timestamp'], args['end_timestamp']]
        auth_data = (args['login'], args['password'], 'organiser')
        return name, columns, query, placeholders, True, auth_data


    def user(self, name, args):
        """
        (*O) user <login> <password> <newlogin> <newpassword>
        """
        columns = []
        query = 'SELECT create_user(%s, %s)'
        placeholders = [args['newlogin'], args['newpassword']]
        auth_data = (args['login'], args['password'], 'organiser')
        return name, columns, query, placeholders, True, auth_data


    def talk(self, name, args):
        """
        (*O) talk <login> <password> <speakerlogin> <talk> <title> <start_timestamp>
                  <room> <initial_evaluation> <eventname>
        """
        columns = []
        query = 'INSERT INTO talk(id, userid, eventid, status, title, room, start_timestamp)' + \
                'VALUES(%s, %s, %s, %s, %s, %s, %s)' + \
                'ON CONFLICT (id) DO UPDATE ' + \
                'SET userid = excluded.userid, title = excluded.title,' + \
                "start_timestamp = excluded.start_timestamp, status = 'accepted';" + \
                'INSERT INTO user_talk_rating(userid, talkid, rating)' + \
                'VALUES(%s, %s, %s)'
        placeholders = [args['talk'], args['speakerlogin'], args['eventname'],
                        'accepted', args['title'], args['room'], args['start_timestamp'],
                        # second query:
                        args['login'], args['talk'], args['initial_evaluation']]
        auth_data = (args['login'], args['password'], 'organiser')
        return name, columns, query, placeholders, True, auth_data


    def register_user_for_event(self, name, args):
        """
        (*U) register_user_for_event <login> <password> <eventname>
        """
        columns = []
        query = 'INSERT INTO user_registered_at_event(userid, eventid) VALUES(%s, %s)'
        placeholders = [args['login'], args['eventname']]
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, True, auth_data


    def attendance(self, name, args):
        """
        (*U) attendance <login> <password> <talk>
        """
        columns = []
        query = 'INSERT INTO user_present_at_talk(userid, talkid) VALUES(%s, %s)'
        placeholders = [args['login'], args['talk']]
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, True, auth_data


    def evaluation(self, name, args):
        """
        (*U) evaluation <login> <password> <talk> <rating>
        """
        columns = []
        query = 'INSERT INTO user_talk_rating(userid, talkid, rating) VALUES(%s, %s, %s)' + \
                ' ON CONFLICT (userid, talkid) DO UPDATE SET rating = excluded.rating'
        placeholders = [args['login'], args['talk'], args['rating']]
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, True, auth_data


    def reject(self, name, args):
        """
        (O) reject <login> <password> <talk>
        """
        columns = []
        query = 'UPDATE talk SET status = ' + \
                "CASE WHEN status='awaiting' OR status='rejected' THEN 'rejected' " + \
                "ELSE 'accepted' END WHERE id=%s"
        placeholders = [args['talk']]
        auth_data = (args['login'], args['password'], 'organiser')
        return name, columns, query, placeholders, True, auth_data


    def proposal(self, name, args):
        """
        (U) proposal  <login> <password> <talk> <title> <start_timestamp> <eventname>
        """
        columns = []
        query = 'INSERT INTO talk(id, userid, eventid, title, start_timestamp)' + \
                'VALUES(%s, %s, %s, %s, %s)'
        placeholders = [args['talk'], args['login'], args['eventname'],
                        args['title'], args['start_timestamp']]
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, True, auth_data


    def friends(self, name, args):
        """
        (U) friends <login1> <password> <login2>
        """
        columns = []
        query = 'INSERT INTO invitation_friend_of(userid1, userid2) VALUES(%s, %s)'
        placeholders = [args['login1'], args['login2']]
        auth_data = (args['login1'], args['password'], 'participant')
        return name, columns, query, placeholders, True, auth_data


    # queries not modifying database:
    def user_plan(self, name, args):
        """
        (*N) user_plan <login> <limit>
        Return attributes: <login> <talk> <start_timestamp> <title> <room>
        """
        columns = ['login', 'talk', 'start_timestamp', 'title', 'room']
        query = 'SELECT ue.userid, talk.id, start_timestamp, title, room ' + \
                'FROM user_registered_at_event ue ' + \
                'JOIN talk ON (ue.eventid = talk.eventid) ' + \
                "WHERE ue.userid = %s AND status = 'accepted' " + \
                'AND start_timestamp >= CURRENT_TIMESTAMP ' + \
                'ORDER BY start_timestamp ' + \
                ('LIMIT %s' if args['limit'] > 0 else '')
        placeholders = [args['login'], args['limit']] if args['limit'] > 0 else [args['login']]
        auth_data = None
        return name, columns, query, placeholders, False, auth_data


    def day_plan(self, name, args):
        """
        (*N) day_plan <timestamp>
        Returned attributes: <talk> <start_timestamp> <title> <room>
        """
        columns = ['talk', 'start_timestamp', 'title', 'room']
        query = 'SELECT id, start_timestamp, title, room FROM talk ' + \
                'WHERE start_timestamp::date = %s::date ' + \
                "AND status = 'accepted' " + \
                'ORDER BY room, start_timestamp'
        placeholders = [args['timestamp']]
        auth_data = None
        return name, columns, query, placeholders, False, auth_data


    def best_talks(self, name, args):
        """
        (*N) best_talks <start_timestamp> <end_timestamp> <limit> <all>
        Returned attributes: <talk> <start_timestamp> <title> <room>
        """
        columns = ['talk', 'start_timestamp', 'title', 'room']
        query = 'SELECT talkid, start_timestamp, title, room, avg(rating) AS avgrate ' + \
                'FROM user_talk_rating ut ' + \
                'JOIN talk ON (ut.talkid = talk.id) ' + \
                "WHERE start_timestamp BETWEEN %s AND %s AND status = 'accepted' " + \
                ('AND ut.userid IN ' + \
                 '(SELECT userid ' + \
                 'FROM user_present_at_talk ' + \
                 'WHERE talkid=talk.id)' if args['all'] == 0 else '') + \
                'GROUP BY talkid, start_timestamp, title, room ' + \
                'ORDER BY avgrate DESC ' + \
                ('LIMIT %s' if args['limit'] > 0 else '')
        print(query)
        placeholders = [args['start_timestamp'], args['end_timestamp']]
        placeholders += [args['limit']] if args['limit'] > 0 else []
        auth_data = None
        return name, columns, query, placeholders, False, auth_data


    def most_popular_talks(self, name, args):
        """
        (*N) most_popular_talks <start_timestamp> <end_timestamp> <limit>
        Returned attributes: <talk> <start_timestamp> <title> <room>
        """
        columns = ['talk', 'start_timestamp', 'title', 'room']
        query = 'SELECT id, start_timestamp, title, room, count(upt.userid) AS people ' + \
                'FROM talk JOIN user_present_at_talk upt ON (talk.id = upt.talkid) ' + \
                "WHERE start_timestamp BETWEEN %s AND %s AND status = 'accepted' " + \
                'GROUP BY id, start_timestamp, title, room ' + \
                'ORDER BY people DESC ' + \
                ('LIMIT %s' if args['limit'] > 0 else '')
        placeholders = [args['start_timestamp'], args['end_timestamp']]
        placeholders += [args['limit']] if args['limit'] > 0 else []
        auth_data = None
        return name, columns, query, placeholders, False, auth_data


    def attended_talks(self, name, args):
        """
        attended_talks <login> <password>
        Returned attributes: <talk> <start_timestamp> <title> <room>
        """
        columns = ['talk', 'start_timestamp', 'title', 'room']
        query = 'SELECT talkid, start_timestamp, title, room ' + \
                'FROM user_present_at_talk upt JOIN talk ON (upt.talkid = talk.id) ' + \
                "WHERE status = 'accepted' AND upt.userid = %s"
        placeholders = [args['login']]
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, False, auth_data


    def abandoned_talks(self, name, args):
        """
        abandoned_talks <login> <password>  <limit>
        Returned attributes: <talk> <start_timestamp> <title> <room> <number>
        """
        columns = ['talk', 'start_timestamp', 'title', 'room', 'number']
        query = 'WITH absent_people AS (' + \
                '(SELECT id AS talkid, ue.userid FROM user_registered_at_event ue ' + \
                'JOIN talk ON (talk.eventid = ue.eventid) ' + \
                "WHERE status = 'accepted') " + \
                'EXCEPT (SELECT talkid, userid FROM user_present_at_talk)) ' + \
                'SELECT id, start_timestamp, title, room, count(ap.userid) AS "number" ' + \
                'FROM talk JOIN absent_people ap ON (ap.talkid = talk.id) ' + \
                "WHERE status = 'accepted' " + \
                'GROUP BY id, start_timestamp, title, room ' + \
                'ORDER BY "number" DESC' + \
                ('LIMIT %s' if args['limit'] > 0 else '')
        placeholders = [args['limit']] if args['limit'] > 0 else []
        auth_data = (args['login'], args['password'], 'organiser')
        return name, columns, query, placeholders, False, auth_data


    def recently_added_talks(self, name, args):
        """
        (N) recently_added_talks <limit>
        Returned attributes: <talk> <speakerlogin> <start_timestamp> <title> <room>
        """
        columns = ['talk', 'speakerlogin', 'start_timestamp', 'title', 'room']
        query = 'SELECT id, userid, start_timestamp, title, room ' + \
                "FROM talk WHERE status = 'accepted' " + \
                "ORDER BY registration_timestamp DESC " + \
                ('LIMIT %s' if args['limit'] > 0 else '')
        placeholders = [args['limit']] if args['limit'] > 0 else []
        auth_data = None
        return name, columns, query, placeholders, False, auth_data


    def proposals(self, name, args):
        """
        (O) proposals <login> <password>
        Returned attributes: <talk> <speakerlogin> <start_timestamp> <title>
        """
        columns = ['talk', 'speakerlogin', 'start_timestamp', 'title']
        query = 'SELECT id, userid, start_timestamp, title FROM talk ' + \
                "WHERE status = 'awaiting' "
        placeholders = []
        auth_data = (args['login'], args['password'], 'organiser')
        return name, columns, query, placeholders, False, auth_data


    def friends_talks(self, name, args):
        """
        (U) friends_talks <login> <password> <start_timestamp> <end_timestamp> <limit>
        Returned attributes: <talk> <speakerlogin> <start_timestamp> <title> <room>
        """
        columns = ['talk', 'speakerlogin', 'start_timestamp', 'title', 'room']
        query = 'SELECT id, userid, start_timestamp, title, room ' + \
                'FROM talk ' + \
                "WHERE status = 'accepted' AND userid IN (" + \
                '(SELECT userid1 FROM friend_of WHERE userid2 = %s) UNION ' + \
                '(SELECT userid2 FROM friend_of WHERE userid1 = %s)) ' + \
                'AND start_timestamp BETWEEN %s AND %s'
        placeholders = [args['login'], args['login'],
                        args['start_timestamp'], args['end_timestamp']]
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, False, auth_data


    def friends_events(self, name, args):
        """
        (U) friends_events <login> <password> <eventname>
        Returned attributes: <login> <eventname> <friendlogin>
        """
        columns = ['login', 'eventname', 'friendlogin']
        query = '(SELECT userid1, ue.eventid, userid2 FROM friend_of ' + \
                'JOIN user_registered_at_event ue ON (ue.userid = userid1) ' + \
                'JOIN user_registered_at_event ue2 ON (ue2.userid = userid2) ' + \
                'WHERE ue2.eventid = ue.eventid AND userid1 = %s) UNION ' + \
                '(SELECT userid1, ue.eventid, userid2 FROM friend_of ' + \
                'JOIN user_registered_at_event ue ON (ue.userid = userid1) ' + \
                'JOIN user_registered_at_event ue2 ON (ue2.userid = userid2) ' + \
                'WHERE ue2.eventid = ue.eventid AND userid2 = %s)'
        placeholders = [args['login'], args['login']]
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, False, auth_data


    def recommended_talks(self, name, args):
        """
        (U) recommended_talks <login> <password> <start_timestamp> <end_timestamp> <limit>
        Returned attributes: <talk> <speakerlogin> <start_timestamp> <title> <room> <score>
        """
        columns = ['talk', 'speakerlogin', 'start_timestamp', 'title', 'room', 'score']
        query = 'SELECT id, talk.userid, start_timestamp, title, room, ' + \
                '(avg(rating) * count(up.userid))::int AS "score" ' + \
                'FROM talk JOIN user_talk_rating ur ON (ur.talkid = talk.id) ' + \
                'JOIN user_present_at_talk up ON (up.talkid = talk.id) ' + \
                "WHERE status = 'accepted' AND start_timestamp BETWEEN %s AND %s " + \
                'GROUP BY id, talk.userid, start_timestamp, title, room ' + \
                'ORDER BY score DESC ' + \
                ('LIMIT %s' if args['limit'] > 0 else '')
        placeholders = [args['start_timestamp'], args['end_timestamp']]
        placeholders += [args['limit']] if args['limit'] > 0 else []
        auth_data = (args['login'], args['password'], 'participant')
        return name, columns, query, placeholders, False, auth_data


    def template(self, name, args):
        columns = []
        query = ''
        placeholders = []
        #auth_data =,
        return name, columns, query, placeholders, True, auth_data
