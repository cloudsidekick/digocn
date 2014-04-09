digocn
========

A simple Python interface to the Digital Ocean cloud API

This library is simply client interface to the Digital Ocean web service
with no abstraction of droplets, images, etc. It was created simply to 
make effecient calls to Digital Ocean and to get back the response in dict format
as opposed to Python objects like some of the other client-side Python
APIs use. The purpose of this library is to allow the developer to stay
as close to the Digital Ocean API as possible.

If this meets your needs, great. Otherwise, here are three others 
I found that you may want to explore:

Pontoon:
https://github.com/duggan/pontoon

Dop:
https://github.com/ahmontero/dop

Python-Digitalocean
https://github.com/koalalorenzo/python-digitalocean

Samples
========

```
import time
from digocn import digocn
client_id = "lskfjjerj3049co3c34jf3jf34j"
api_key = "kjfojf34fmfi2jlkj095flkskls"

def check_event_status(event_id):
    """A helper that will loop until the even is done"""

    status = None
    while status != "done":
        time.sleep(10)
        r = conn.call("events", action=None, subject=event_id)
        print r
        status = r["event"]["action_status"]
    return


# define the connection
conn = digocn.DigOcnConn(client_id, api_key, debug=False)

# list all sizes
r = conn.call("sizes")
for s in r["sizes"]:
    print s

# list all images
r = conn.call("images")
for i in r["images"]:
    print i

# list all images
r = conn.call("regions")
for z in r["regions"]:
    print z

my_droplets = []

# create a new droplet
r = conn.call("droplets", "new", params={"name":"test1", "size_id": "66", "image_id" : 962304, "region_id" : 4})
event_id = r["droplet"]["event_id"]
id = r["droplet"]["id"]
my_droplets.append(id)
print "Event id is %s" % (event_id)

# loop until the event is done
check_event_status(event_id)

# create a new droplet using the slugs
r = conn.call("droplets", "new", params={"name":"test1", "size_slug": "512MB", "image_slug" : "ubuntu-12-04-x64", "region_slug" : "nyc2"})
event_id = r["droplet"]["event_id"]
id = r["droplet"]["id"]
my_droplets.append(id)
print "Event id is %s" % (event_id)

# loop until the event is done
check_event_status(event_id)


# list all droplets
d = conn.call("droplets")
for i in d["droplets"]:
    print i

# destroy the ones we created
for d in my_droplets:
    r = conn.call("droplets", "destroy", d)
    print r
```

