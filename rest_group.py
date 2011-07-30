
import sr
from types import *
from rest_request import restRequest

class group(restRequest):

    def __init__(self):
        self._mapping = { "add"          : self.create
                        , "rm"           : self.delete
                        , "search"       : self.search
                        , "info"         : self.info
                        , "listmembers"  : self.listMembers
                        , "addmembers"   : self.addMembers
                        , "delmembers"   : self.removeMembers
                        }

    def validate(self, command, user):
        return False

    def _get_group(self, gid):
        group = sr.groups.group(gid)
        if not group.in_db:
            raise Exception("Group '%s' not in the database." % uid)
        return group

    def create(self, name, description):
        """
        Create a new group.
        @param name (string): The name of the group to create.
        @param description (string): A description of the new group.
        """

        # TODO: do something with the description
        g = sr.group( name )

        if g.in_db:
            raise Exception("Group '%s' already exists" % name)

        if not g.save():
            raise Exception("Failed to create group '%s'" % name)

    def delete(self, name):
        """
        Delete a group.
        @param name (string): Name of the group to delete.
        """

        g = self._get_group(name)

        if not g.rm():
            raise Exception("Could not remove group '%s'." % name)

    def info(self, name):
        """
        Get information about a group.
        @param name (string): The name of the group of interest.
        @returns name (string): The name of the group.
        @returns description (string): The description of the group.
        """

        g = self._get_group(name)

        return dict(name=g.name, description='TODO')

    def search(self, regexp):
        """
        Search for groups.
        @param regexp (string): Regexp for matching against group name.
        @returns groups (list of strings): The names of the groups that match the search.
        """

        assert type(regexp) is StringType, 'Can only search by string'

        return sr.groups.list()

    def listMembers(self, name):
        """
        List the members of a group.
        @param name (string): The name of the group of interest.
        @return users (list of strings): The usernames of the members of the group.
        """

        g = self._get_group(name)

        return g.members

    def addMembers(self, name, users):
        """
        Add members to a group.
        @param name (string): The name of the group to add to.
        @param users (list of strings): The users to add to the group.
        """

        assert type(users) is ListType, "Can only add lists of users"
        assert len(users) > 0, "Nothing to do"

        g = self._get_group(name)

        f = g.user_add(users)
        g.save()

        if len(f) > 0:
            raise Exception("WARNING: The following users were not found and so were not added: "+", ".join(f))

    def removeMembers(self, name, users ):
        """
        Remove members from a group.
        @param name (string): The name of the group to remove the users from.
        @param users (list of strings): The usernames of the users to remove from the group.
        """

        assert type(users) is ListType, "Can only add lists of users"
        assert len(users) > 0, "Nothing to do"

        g = self._get_group(name)

        # TODO: verify that the users are in the group?
        # TODO: verify that the users exist?
        g.user_rm( users )
        g.save()
