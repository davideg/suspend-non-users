import os
import sys

from github3 import enterprise_login
from requests import put


class Suspender:

    def __init__(self, url, access_token, should_verify=False):
        self.ghe_url = url
        self.token = access_token
        self.should_verify = should_verify
        self.hub = enterprise_login(token=access_token, url=url)

    def find_non_users(self):

        def _find_non_users_gen():
            for user in self.hub.all_users():
                if user.type != 'Organization':
                    user_detail = self.hub.user(user.login)
                    if not self.is_suspended(user_detail) and \
                       self.user_has_no_activity(user_detail):
                        yield user.login

        return _find_non_users_gen()

    def is_suspended(self, user_detail):
        return user_detail.as_dict().get('suspended_at') is not None

    def user_has_no_activity(self, user_detail):
        return 0 == (user_detail.disk_usage +
                     user_detail.public_repos_count +
                     user_detail.public_gists +
                     user_detail.total_private_repos +
                     user_detail.total_private_gists)

    def suspend_user(self, user):
        return put(self.ghe_url + ('/' if self.ghe_url[-1] != '/' else '')
                                + 'api/v3/'
                                + 'users/{0}/suspended'.format(user)
                                + '?access_token={0}'.format(self.token))

    def suspend_non_users(self):
        for user in self.find_non_users():
            if self.should_verify:
                print 'Should {0} be suspended? [Y/n]'.format(user)
                answer = raw_input()
                if answer == 'y' or answer == 'Y':
                    self.suspend_user(user)
                    print 'Suspended {0}'.format(user)
            else:
                print 'Suspended {0}'.format(user)
                self.suspend_user(user)


if __name__ == '__main__':
    should_verify = False
    usage = 'usage: suspend_non_users.py <ghe_url> [option]\n\nOptions:\n-i\tVerify before suspending each user'
    if len(sys.argv) < 2:
        print usage
        sys.exit(1)
    ghe_url = sys.argv[1]
    token = os.environ.get('GHE_ACCESS_TOKEN')
    if len(sys.argv) == 3:
        if sys.argv[2] == '-i':
            should_verify = True
        else:
            print usage
            sys.exit(1)
    if token:
        s = Suspender(ghe_url, token, should_verify)
        s.suspend_non_users()
    else:
        sys.stderr.write('Please provide your access token in $GHE_ACCESS_TOKEN\n')
        sys.exit(1)
