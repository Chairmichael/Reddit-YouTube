#/usr/bin/env 
# ytHaikuBot.py

import praw
import configparser, csv

def get_posts_info(reddit):
    posts = [ ]
    # get a bunch of YouTubeHaiku posts
    for p in reddit.subreddit('youtubehaiku').top(limit=100):
        posts.append([p.score, p.num_comments, p.url])
    return posts

def get_vid_length(id, start=0, end=0):
    return 0

def get_id(url):
    part = url.split('/')[-1].split('watch?v=')[-1]
    vid_id = part.split('?t=')[0]
    # get the start/end time
    time = part.split('?t=')
    if len(time) == 1:
        return [vid_id, 0, 0]
    else:
        t = ''.join([i for i in time[1] if not i.isalpha()])
        return [vid_id, t, 0]

def main():
    config = configparser.ConfigParser()
    config.read('credentials.ini')
    redditCreds = config['Auth-Reddit']
    redditAPI = praw.Reddit(client_id=redditCreds['client_id'],
                            client_secret=redditCreds['client_secret'],
                            password=redditCreds['password'],
                            user_agent=redditCreds['user_agent'],
                            username=redditCreds['username'])
    output_file = 'data.csv'

    # get list of post info
    post_info = get_posts_info(redditAPI)

    # get video id
    for p in post_info:
        for x in get_id(p[2]): p.append(x)

    # get video length
    for p in post_info:
        p.append(get_vid_length(p[3]))

    # log info in csv
    with open('output_file.csv', 'w', newline='') as csvfile:
        fieldnames = ['score', 'num_comments', 'url', 'id', 'start', 'end', 'length']
        output = csv.DictWriter(csvfile, fieldnames=fieldnames)
        output.writeheader()

        for post in post_info:
            # change into dictionary to work with csv
            d = dict(zip(fieldnames, post))
            output.writerow(d)

if __name__ == '__main__':
    import os, sys
    main()
