import requests
from credentials import *
import time
import json
import pprint
import urllib
import os

POSTS_PER_REQUEST = 100
POST_FILE = "done_images.txt"

last_name = "" # for pagination
for i in range(10): # arbitrary, but who needs more than 1000 images at a time
    id_dict = {}
    
    with open(POST_FILE, "r") as f:
        done_posts = f.readlines()
    done_posts = [p.strip() for p in done_posts]
    
    # This is the way reddit pagination works, you need to specify the number of posts after a certain post - I'm saving the last one of every loop
    print("getting {0} posts after {1}".format(
        POSTS_PER_REQUEST, 
        last_name)
        )
    
    # GET request
    r = requests.get(
        'https://www.reddit.com/r/wallpaper/new/.json?limit={0}&after={1}'.format( 
            POSTS_PER_REQUEST, 
            last_name
            ), 
        verify=False, # Not recommended for requests involving your credentials
        headers={"User-agent": USER_AGENT}
        )

    subreddit_dict = r.json() 
    # We have a dictionary of our subredit page
    posts = subreddit_dict["data"]["children"]
    for p in posts:
        post_dict = p["data"]
        # get the ID of our post
        post_id = post_dict["id"]
        # ensure we haven't already done it in another instance
        if not post_id in done_posts:
            id_dict[post_id] = post_dict["url"]
            with open(POST_FILE, "a") as f:
                f.write(post_id+"\n")

    # Note down name of last post for pagination
    last_name = posts[-1]["data"]["name"]
    print("request made and posts received")
    
    # Now we have a list of posts, let's get the images!
    for post_id in id_dict.keys():
        print(post_id)
        # get the url from our post dictionary
        url = id_dict[post_id]
        # get the extension of the image, if present
        ext = url.split(".")[-1]
        # open the url
        req = urllib.request.urlopen(url) 
        # check that the page we have requested is the page we go to, not "https://i.imgur.com/removed.png"!
        finalurl = req.geturl() 
        if ext.lower() in ["jpg", "png", "bmp"] and finalurl == url: # check file is an image, and we haven't been redirected
            print("getting and saving {0}".format(url))
            urllib.request.urlretrieve(url, os.path.join("..","..","Backgrounds",post_id+"."+ext))
        else:
            print("rejected: extension: {0}, url {1}".format(ext, finalurl))
    time.sleep(2.1)

