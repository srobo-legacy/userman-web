
import sr
import re
from types import *
from rest_request import restRequest

'''
class restGroup(restRequest):
    _mapping = { "info"     : user.members
               , "add"      : user.create
               , "rm"       : user.delete
               , "search"   : user.search
               , "addusers" : user.addusers
               , "delusers" : user.delusers
               }

    def handle(self, command, kwargs):
        return None

    def validate(self, command, user):
        return False
'''

def def_uidBuilder(first_name, last_name):
    return first_name + last_name

class user:
    uidBuilder = None

    def _names_to_id(self, first, last):
        if self.uidBuilder is None:
            return def_uidBuilder(first, last)
        else:
            self.uidBuilder(first, last)

    def _get_user(self, uid):
        user = sr.users.user(uid)
        if not user.in_db:
            raise Exception("User '%s' not in the database." % uid)
        return user

    def create(self, first_name, last_name, email):
        """
        Create a user.
        @param first_name (string): The first name of the new user.
        @param last_name (string): The last name of the new user.
        @param email (string): The email address of the new user.
        @returns name (string): The username of the new user.
        """

        username = self._names_to_id(first_name, last_name)

        u = sr.users.user( username )

        if u.in_db:
            raise Exception("User '%s' already exists" % username)

        u.cname = first_name
        u.sname = last_name
        u.email = email

        if not u.save():
            raise Exception("Failed to create user '%s'" % username)

        return username

    def search(self, search):
        """
        Search for a user, searches in all available fields, an empty search lists all users.
        @param search (string): The string to search for.
        @param users (list of strings): The names of the users that match the search.
        """
        assert type(search) is StringType, 'Can only search by string'

        userList = sr.users.list()
        matches = []
        # TODO: actual searching outside the uid
        for user in userList:
            if re.search(search, user) is not None:
                matches.append(user)

        return matches

    def delete(self, name):
        """
        Delete a user.
        @param name (string): The username of the user to be deleted.
        """
        assert type(name) is StringType, 'Can only remove by string'

        u = self._get_user(name)
        groups = u.groups()

        if not u.delete():
            raise Exception("Could not remove user '%s'." % name)

        for group in groups:
            g = sr.group(group)
            g.user_rm(name)
            g.save()

    def info(self, name):
        """
        Get info about a specific user.
        @param name (string): The username of the user of interest.
        @returns first_name (string): The first name of the new user.
        @returns last_name (string): The last name of the new user.
        @returns email (string): The email address of the new user.
        @returns groups (list of strings): The names of the groups that the user is a member of.
        """

        u = self._get_user(name)
        return { 'first_name'   : u.cname
               , 'last_name'    : u.sname
               , 'email'        : u.email
               , 'groups'       : u.groups()
               }

    def passwd(self, name, password):
        """
        Set a user's password.
        @param name (string): The name of the user to change the password of.
        @param password (string): The new password to set.
        """

        u = self._get_user(name)

        if not u.set_passwd( new = password ):
            raise Exception("Failed to set password for user '%s'" % name)

    def rand_pass(self, name):
        """
        Set a random password for a user.
        @param name (string): The name of the user to give a random password.
        # is this not made redundant by #userpasswd?
        """

        new_passwd = sr.users.GenPasswd()
        u = self.passwd(name, new_passwd)

        # TODO: how do we want to handle this bit?
        # mailer.send_template( "new-password", u, { "PASSWORD": new_passwd } )
