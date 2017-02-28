#!/usr/bin/env python

import praw
import time

settings = {
    'username': 'username',
    'password': 'password',
    'user_agent': 'angry /r/politics robot',
    'subreddit': 'politics',
}

r = praw.Reddit(user_agent=settings['user_agent'])

r.login(settings['username'], settings['password'])

submissions = r.get_subreddit(settings['subreddit']).get_hot(limit=100)

for s in submissions:
    # Skip if post has already been downvoted
    if not s.likes and s.likes is not None:
        continue

    s.downvote()
    print("Downvoted: '{}'".format(s.title[0:70]))

    time.sleep(2)
