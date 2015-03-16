#! /usr/bin/env python3

# No more overview implicit section
# No more history implicit section?
from wikia import wikia
import praw

bot = praw.AuthenticatedReddit("Testing")
bot.login("autowikiabot", "I lke JSON")
me = bot.get_redditor("autowikiabot")
for post in me.get_comments():
    try:
        # Get the url for the other two
        start, end = post.body.find("("), post.body.find(")")
        url = post.body[start + 1: end]
        print("URL: ", url)
        # Get the subwikia
        start, end = url.find("//"), url.find(".wikia.com")
        if end == -1: continue
        sub_wikia = url[start + 2: end]
        # Get the title
        start = url.rfind("/")
        title = url[start + 1:]
        title = title.replace("%20", " ")
        title = title.replace("%27", "'")

        # Open up the wikia page
        print("Sub-wikia: ", sub_wikia, "Title: ", title)
        page = wikia.page(sub_wikia, title)
        summary = page.summary
        if not summary:
            continue
        # If the summary is not complete, get the section summary
        if summary.endswith("..."):
            summary = page.section(page.sections[0])
        # So it prints properly
        summary = summary.encode("ascii", "ignore")
        # So it prints properly
        body = post.body.encode("ascii", "ignore")
        print ("NEW SUMMARY:")
        print(summary)
        input("\n>")
    except Exception as e:
        print("ERROR: ", e)
