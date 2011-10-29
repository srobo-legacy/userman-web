
import sr
import re
from types import *
from datetime import timedelta
from rest_request import restRequest
from securetoken import Token

def def_uidBuilder(first_name, last_name):
    return first_name + last_name

class user(restRequest):
    uidBuilder = None

    def __init__(self):
        self._mapping = { "info"        : self.info
                        , "add"         : self.create
                        , "rm"          : self.delete
                        , "search"      : self.search
                        , "passwd"      : self.passwd
                        , "send_pass_token" : self.send_pass_token
                        }

    def validate(self, command, user):
        return False

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

    def passwd(self, name, new_password, old_password = None, pass_token = None):
        """
        Set a user's password.
        @param name (string): The name of the user to change the password of.
        @param new_password (string): The new password to set.
        @param old_password (string): The old password for confirmation.
        @param pass_token (string): A password reset token.
        Note that only one of old_password and pass_token should be supplied,
        the other will be checked against None to determine which to use.
        """

        if pass_token is None and old_password is None:
            raise Exception("Cannot change password without verification: requires either the old password or a password reset token")

        u = self._get_user(name)

        if pass_token is None:
            # use the (given) old password as part of the reset
            if not u.set_passwd(old_password, new_password):
                raise Exception("Failed to set password for user '%s'" % name)
        else:
            tok = securetoken.load(pass_token)
            if tok is None or tok.name != name:
                raise Exception("Invalid pass token for user '%s'" % name)

            if tok.age() > timedelta(minutes=60):
                raise Exception("Pass token out of date")

            if not u.set_passwd(new=new_password):
                raise Exception("Failed to set password for user '%s'" % name)

    def send_pass_token(self, name):
        """
        Sends the user a forgotten password token, suitable for supplying to /user/passwd.
        These are stored by the server against a user name,
        and are only valid for a fixed duration, probably under an hour.
        @param name (string): The name of the user to reset the password of and to send the email to.
        TODO: include user id verification? Confirm school based on random selection of 3?
        """

        # TODO: ident validation
        info = dict(name=name)
        token = securetoken.Token(info).encrypt()

        # TODO: how do we want to handle this bit?
        # mailer.send_template( "pass_token", u, { "TOKEN": token } )
