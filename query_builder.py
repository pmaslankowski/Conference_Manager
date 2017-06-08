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


    def template(self, name, args):
        columns = []
        query = ''
        placeholders = []
        #auth_data =,
        return name, columns, query, placeholders, True, auth_data
