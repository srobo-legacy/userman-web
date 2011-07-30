
from rest_user import user, def_uidBuilder
from rest_group import group
from types import *

## User tests:

fn = 'first'
ln = 'last'
addr = 'fl@sr.org'
uid = def_uidBuilder(fn, ln)

def test_user(u):
    print """Check valid searches"""
    for srch in ['zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', '', '#', '@@', uid]:
        ret = u.search(srch)
        assert type(ret) is ListType, 'Search should always return a list: %s' % ret

    print """Try adding a user."""
    ret = u.create(fn, ln, addr)
    assert ret == uid, "wrong result"

    print """Try adding the same user again -- should error."""
    ret = None
    try:
        ret = u.create(fn, ln, addr)
    except:
        pass
    else:
        assert ret is None, 'Should not be able to add same user twice!'

    print """Check the user we just added is listed."""
    # TODO: also search by email
    for srch in [uid, fn, ln]: #, addr]:
        res = u.search(srch)
        assert uid in res, "Failed to find user when searching for '%s'" % srch

    print """Get info for our user."""
    info = u.info(uid)
    assert info == dict(first_name=fn, last_name=ln, email=addr, groups=[]), 'Got wrong info for user'

    print """Try removing a user -- we just added this one."""
    u.delete(uid)

    print """Try removing the same user again -- should error."""
    try:
        u.delete(uid)
    except:
        pass
    else:
        assert False, 'Should not be able to add same user twice!'

## Group tests:

gp1 = 'first-test-group'
gp2 = 'second-test-group-A'
gp3 = 'second-test-group-B'

def test_group(g, gid):
    print """Check valid searches"""
    for srch in ['zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', '', '#', '@@', gid]:
        ret = g.search(srch)
        assert type(ret) is ListType, 'Search should always return a list: %s' % ret

    print """Try adding a group."""
    dn = 'Jams'
    g.create(gid, dn)

    print """Try adding the same group again -- should error."""
    try:
        g.create(gid, 'Beans')
    except:
        pass
    else:
        assert False, 'Should not be able to add same group twice!'

    print """Check the group we just added is listed."""
    for srch in [gid, '*test*', 'first*']:
        res = g.search(srch)
        assert gid in res, "Failed to find group when searching for '%s'" % srch

    print """Get info for our group."""
    info = g.info(gid)
    exp = dict(name=gid, description=dn)
    # Not yet implemented
    # assert exp == info, "Got wrong info for group:\n Expected '%s',\n Actual   '%s'" % (exp, info)

    print """List group members -- should be none at the start."""
    members = g.listMembers(gid)
    assert members == [], "There should be no members at the start, got '%s'" % members

    print """Try listing members of a non-existent group -- should error."""
    members = None
    try:
        members = g.listMembers(gid+'42')
    except:
        pass
    else:
        assert members is None, "Should not be able to query members of a non-existent group, got '%s'" % members

    print """Add a group member."""
    g.addMembers(gid, [uid])
    members = g.listMembers(gid)
    assert uid in members, "Member not found in group after addition, got '%s'" % members

    print """Try adding the same member again -- should error."""
    try:
        g.addMembers(gid, [uid])
    except:
        pass
    else:
        pass
        # Not yet implemented
        # assert False, "Should not be able to add an existing member to a group"

    print """Add a group member."""
    g.removeMembers(gid, [uid])
    members = g.listMembers(gid)
    assert uid not in members, "Member found in group after removal, got '%s'" % members

    print """Try removing the same member again -- should error."""
    try:
        g.removeMembers(gid, [uid])
    except:
        pass
    else:
        pass
        # Not yet implemented
        # assert False, "Should not be able to remove member not part of a group"

    print """Try removing a group -- we just added this one."""
    g.delete(gid)

    print """Try removing the same group again -- should error."""
    try:
        g.delete(gid)
    except:
        pass
    else:
        assert False, 'Should not be able to add same group twice!'


## Run the tests
if __name__ == '__main__':
    u = user()
    # remove the user if they're there from a previous run:
    if uid in u.search(uid):
        u.delete(uid)

    g = group()
    # Ensure the groups are present:
    for gp in [gp1, gp2, gp3]:
        if gp in g.search(gp):
            g.delete(gp)

    print "-- User test --"
    try:
        test_user(u)
    except AssertionError as ae:
        print ' - Fail! - '
        raise
    except Exception as e:
        print ' - Exploded - '
        raise
    else:
        print ' - Pass - '

    # We need a user to test the group memberships
    u.create(fn, ln, addr)

    print "-- Group test --"
    try:
        test_group(g, gp2)
    except AssertionError as ae:
        print ' - Fail! - '
        raise
    except Exception as e:
        print ' - Exploded - '
        raise
    else:
        print ' - Pass - '

