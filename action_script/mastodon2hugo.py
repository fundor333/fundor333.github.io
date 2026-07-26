# Mastodon 2 Hugo
# By Francesco Maida (https://github.com/fmaida)
#
# This script will download a copy of the
# .well-known/webfinger file from your mastodon account
# and will place it under your 'static' directory
#
# Why you should use it?
# ----------------------
# This way, if any user try to search on mastodon by using
# your domain, Hugo will tell Mastodon to fetch the proper
# mastodon account
#
# Requires a Hugo Project (https://www.gohugo.io)
# Requires Python 3.7 or higher

import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlretrieve

# Let's try to fetch the Mastodon account
# from the command line argument
if len(sys.argv) > 1:
    account = sys.argv[1]
else:
    # The user didn't provide a Mastodon account
    # Let's ask them for it
    print("Please Enter your Mastodon account")
    account = input("[Example: @name@domain.com]: ")

# Now let's split the mastodon account into
# its username and domain
valid_account = True
domain = None
if len(account) < 8 or account.count("@") != 2:
    # The user didn't provide a valid Mastodon account
    valid_account = False
else:
    domain = account.split("@")[-1]
    if len(domain) < 5:
        # The user didn't provide a valid Mastodon domain
        valid_account = False

# Now let's check if the user provided a valid account
if not valid_account:
    # Sorry, it's a no go.
    print(f"{account!r} doesn't look like a valid Mastodon account.")
    exit(-1)

# If the user provided a valid account,
url = f"https://{domain}/.well-known/webfinger"
url += f"?resource=acct:{account[1:]}"

# Let's prepare some variables with the paths to
# the static and .well-known directories, as well
# as the path to the webfinger file
current_dir = Path.cwd()
static_dir = current_dir / "static"
well_known_dir = static_dir / ".well-known"
webfinger_file = well_known_dir / "webfinger"

# Let's check if a 'static' directory already exists
if not static_dir.exists():
    # Nope. We need to create it
    print(f"Creating static directory at {static_dir!r}")
    static_dir.mkdir(parents=True)

# Let's check if a '.well-known' sub-directory
# already exists inside of the 'static' directory
if not well_known_dir.exists():
    # Nope. We need to create it
    print(f"Creating static/.well-known directory at {well_known_dir!r}")
    well_known_dir.mkdir(parents=True)

# Let's download the Mastodon account's webfinger file
# and place it in the static/.well-known directory
try:
    urlretrieve(url, str(webfinger_file))
except URLError:
    # Uh Oh, something went wrong
    print(f"Couldn't connect to {url!r}")
    quit(-1)

# Everything is done
print("Done! Have a nice day!")
quit(0)
