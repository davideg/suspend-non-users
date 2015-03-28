### Suspend Non Users

This script suspends users that have no repositories or gists on your GitHub Enterprise instance.

#### What problem is this solving?
Sometimes users create accounts on your instance out of curiosity but never create repositories or gists. This script automates the task of checking which users have no data on GitHub Enterprise and suspends them.

#### Known limitations
Note that this script suspends users that have no repository or gist data on a GitHub Enterprise instance but doesn't take into account session activity or whether they created issues, pull requests, or comments.

#### Dependencies

This script relies on:
- [requests](http://docs.python-requests.org/)
- [github3](http://github3py.readthedocs.org/)

#### Usage
[Generate an access token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) for a GitHub Enterprise Admin user and set $GHE_ACCESS_TOKEN to this token:

````
export GHE_ACCESS_TOKEN=<token>
````

You can see usage information by executing the script with no arguments or options:
````
$ python suspend_non_users.py
usage: suspend_non_users.py <ghe_url> [option]

Options:
-i  Verify before suspending each user
````
When you're ready, provide the URL to your GitHub Enterprise instance as the first argument and optionally add `-i` if you'd like to manually verify each suspension:
````
$ python suspend_non_users.py https://my-ghe-host -i
````
