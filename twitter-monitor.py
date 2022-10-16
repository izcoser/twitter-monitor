import wget
from twitter import *
from os import makedirs
from os.path import isfile, isdir, join
from pathlib import Path
import sys
from time import sleep

def find_best_bitrate(variants):
    best = 0
    url = None
    for v in variants:
        if 'bitrate' in v and v['bitrate'] > best:
            best = v['bitrate']
            url = v['url']
    
    return url, best

def download():
    token, token_secret, consumer_key, consumer_secret = open(str(Path.home()) + '/credentials').read().splitlines()[:-1]
    twitter = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret), retry=True)
    screen_name = sys.argv[1]
    log_tweets = len(sys.argv) >= 3 and sys.argv[2] == "--log"
    max_id = int(2e18)

    dir = join('.', screen_name)

    if not isdir(dir):
        makedirs(dir)

    if log_tweets:
        tweet_file = open(dir + "/" + screen_name + "-tweets", "a+", encoding="utf-8")
        
    while True:
        try:
            tweets = twitter.statuses.user_timeline(screen_name=screen_name, count=200, max_id=max_id, include_rts=False, include_entities=True, tweet_mode='extended')
        except:
            continue
        if not tweets or tweets[-1]['id'] == max_id:
            break
        max_id = tweets[-1]['id']
        for t in tweets:
            #print(t['full_text'][:20] + '\t', end='')

            if log_tweets:
                tweet_file.write(f"{t['created_at']}: {t['full_text']}\n")
            print(f"{t['created_at']}: {t['full_text']}")

            if 'entities' not in t.keys() and 'extended_entities' not in t.keys():
                continue
            if 'extended_entities' in t.keys():
                    for m in t['extended_entities']['media']:
                        if 'video_info' in m.keys():
                            url, bitrate = find_best_bitrate(m['video_info']['variants'])
                            fname = url.split('/')[-1].split('?')[0]
                            if not isfile(join(dir, fname)):
                                print(f"Downloading video {fname} ({bitrate}) from tweet at {t['created_at']}")
                                print(url)
                                wget.download(url, dir)
                            else:
                                print(f"{fname} already exists, stopping here.")
                                return
                        else:
                            fname = m['media_url'].split('/')[-1]
                            if not isfile(join(dir, fname)):
                                print(f"Downloading picture {fname} from tweet at {t['created_at']}")
                                wget.download(m['media_url'], dir)
                            else:
                                print(f"{fname} already exists, stopping here.")
                                return
            elif 'media' in t['entities'].keys():
                fname = t['entities']['media'][0]['media_url'].split('/')[-1]
                if not isfile(join(dir, fname)):
                    print(f"Downloading picture {fname} from tweet at {t['created_at']}")
                    wget.download(t['entities']['media'][0]['media_url'], dir)
                else:
                    print(f"{fname} already exists, stopping here.")
                    return
    
    
    if log_tweets:
        tweet_file.close()

while True:
    download()
    sleep(180)
