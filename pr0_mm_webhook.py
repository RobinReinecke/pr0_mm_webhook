import pr0gramm
import requests
import json
import schedule
import time

class pr0_mm:
    """
    Automated class, which posts the newest items from http://pr0gramm.com to an 
    mattermost incoming webhook.
    https://docs.mattermost.com/developer/webhooks-incoming.html
    """
    def __init__(self, webhook_url, Interval, EnableSFW, EnableNSFW, EnableNSFL, EnableTop):
        """
        Initialize the class.
        
        Arguments:
            webhook_url {string} -- Mattermost Webhook URL
            Interval {int} -- Interval the class should check for new posts in minutes
            EnableSFW {bool} -- Enable SFW Filter
            EnableNSFW {bool} -- Enable NSFW Filter
            EnableNSFL {bool} -- Enable NSFL Filter
            EnableTop {bool} -- Enable Top
        """

        self.username = "pr0gramm-bot"
        #example pr0 icon
        self.icon_url = "https://vignette.wikia.nocookie.net/pr0gramm/images/f/fc/Pr0gramm_Logo.svg.png/revision/latest?cb=20150527200407"
        self.url = webhook_url
        self.Interval = Interval
        #pr0gramm settings
        self._API = pr0gramm.Api(EnableSFW, EnableNSFW, EnableNSFL, EnableTop)
        #latest known post from pr0gramm
        self._latest_post_promotion = None

    def start(self):
        """
        Start the posting.
        """

        print("Starting...")

        # get latest post
        latest_post = self._API.get()[0]

        print("Latest Post-ID: " + str(latest_post["id"]))
        # for correct order like on the website safe the "promoted" attribute
        # instead of the ID
        self._latest_post_promotion = latest_post["promoted"]

        schedule.every(self.Interval).minutes.do(self._check)
        while 1:
            schedule.run_pending()
            time.sleep(1)
    
    def _check(self):
        #payload for request
        payload = {"username": self.username, "icon_url": self.icon_url}
        #header for request
        headers = {'content-type': 'application/json'}

        print("Checking for new posts...")
        #fetch latest posts
        posts = self._API.get()

        print("Latest Post-ID: " + str(posts[0]["id"]) + " and Promotion: " + str(posts[0]["promoted"]))
        
        #iterate over posts
        for post in posts:
            # if post isn't later then the known post, skip
            if post["promoted"] <= self._latest_post_promotion:
                continue

            #print the later post
            print("Post found: " + str(post["id"]) + " and Promotion: " + str(post["promoted"]))
            # clone payload
            payload2 = dict(payload)

            post_id = post["id"]
            # get infos for this post
            info = api.info(post_id)

            #send top 3 tags and link to the post to mattermost
            text =  ("**" + info["tags"][0]["tag"] + "**   " +
                        "**" + info["tags"][1]["tag"] + "**   " +
                        "**" + info["tags"][2]["tag"] + "**   " +
                        "\n**Link:** " + "http://pr0gramm.com//" + str(post["id"]) + "\n")
            

            # add Text to payload
            payload2.update({"text": text })
            # send request to webhook
            requests.post(self.url, data=json.dumps(payload2), headers=headers)


            # if the post is an image or gif, post the direct link as additional message 
            # to the webhook. Mattermost only embedds images when they stand alone in a 
            # message.
            if post["image"].endswith((".jpg",".png",".gif")):
                payload2["text"] = "http://img.pr0gramm.com/" + post["image"]
                r = requests.post(url, data=json.dumps(payload2), headers=headers)

        self._latest_post_promotion = posts[0]["promoted"]


