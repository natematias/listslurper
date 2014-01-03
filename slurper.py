import re
import simplejson
import time
import tweepy

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

API = tweepy.API(auth)


def get_users(handle, listname):
    if API.rate_limit_status()['resources']['lists']['/lists/members']['remaining'] < 5:
        print "Rate limit near, going to sleep"
        time.sleep(15*60)

    users = []
    try:
        for member in tweepy.Cursor(API.list_members, handle, listname).items():
            users.append(member)

    except tweepy.error.TweepError:
        print "Did not find list for: " + listname
        return []

    return [{'screen_name' : user.screen_name, 'twitter_id' : user.id} for user in users]


if __name__ == '__main__':
    with open('lists.json', 'r') as fp:
        orgs = simplejson.loads(fp.read())

    for orgname in orgs:
        url = orgs[orgname]
        match = re.match('(https://twitter.com|http://twitter.com)/(.*)/(.*)/members', url)
        if match:
            twitter_handle = match.group(2)
            twitter_list = match.group(3)
            users = get_users(twitter_handle, twitter_list)
            with open('data/'+orgname.replace(' ', '')+'.json', 'w') as wfp:
                wfp.write(simplejson.dumps(users, sort_keys=True, indent=4 * ' '))
        else:
            print "Couldn't parse URL: " + url