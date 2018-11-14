#/usr/bin/env 
# ytHaikuBot.py

import praw
import configparser, csv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def youtube_authenicate(youtubeConfig):
    return build(
        youtubeConfig['YOUTUBE_API_SERVICE_NAME'], 
        youtubeConfig['YOUTUBE_API_VERSION'],
        developerKey=youtubeConfig['DEVELOPER_KEY'])

def reddit_authenicate(redditConfig):
     return praw.Reddit(
        client_id=redditConfig['CLIENT_ID'],
        client_secret=redditConfig['CLIENT_SECRET'],
        password=redditConfig['PASSWORD'],
        user_agent=redditConfig['USER_AGENT'],
        username=redditConfig['USERNAME'])

def get_posts_info(reddit):
    posts = [ ]
    # get a bunch of YouTubeHaiku posts
    for p in reddit.subreddit('youtubehaiku').top(limit=100):
        posts.append([p.score, p.num_comments, p.url])
    return posts

def get_vid_length(yt, start=0, end=0):
    return 0

def parse_url(url):
    part = url.split('/')[-1].split('watch?v=')[-1]
    vid_id = part.split('?t=')[0].split('&t=')[0].split('&feature')[0]
    # get the start/end time
    start = part.split('?t=')[-1].split('&t=')[-1]
    print(type(start))
    if len(start) == 1: start = 0
    else: t = ''.join([i for i in start[1] if not i.isalpha()])

    print(f'url = {url}, id = {vid_id}, start = {start}')
    return [vid_id, start, 0]

def main():
    config = configparser.ConfigParser()
    config.read('credentials.ini')
    # Authenicate Reddit
    redditConfig = config['Auth-Reddit']
    redditAPI = reddit_authenicate(redditConfig)
    # Authenicate YouTube
    youtubeConfig = config['Auth-YouTube']
    youtube = youtube_authenicate(youtubeConfig)

    output_file = 'data.csv'

    # get list of post info
    post_info = get_posts_info(redditAPI)

    # get video id
    for p in post_info:
        for x in parse_url(p[2]): p.append(x)

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
