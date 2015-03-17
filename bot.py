#! /usr/bin/env python3

# Implicit sections change: Only use that if the first section is too small, and even then stick it after the section that is too short.
# Too short in this case is the length of a general description (500 characters).
# If a section is < 500 characters, try to get about that size (up to that size, and then until the end of the first sentence past that point)
# It will be something like this:
#     first_bit = page.section(page.sections[0])
#     second_bit = page.section(implicit_whatever_or_maybe_just_second_paragraph)
#     # chop the second bit so that we only get up to 500 characters
#     second_bit = second_bit[:(500 - len(first_bit))]
#     # Now get where the next period is in that bit. Should use regex to find the next sentence ending punctuation honestly
#     next_period = second_bit.find(".")
#     # Then use that to construct the rest of the second bit
#     second_bit = second_bit[:((500 - len(first_bit)) + next_perid)]
#     # Then stick em together
#     summary = first_bit + second_bit
#     return summary

#     The way the summary works is trying to get 500 characters from the first
#     couple of sections. If we use the above method, we can avoid the "...".
#     Though I think the implicit_section needs to simple be replaced by the next
#     section after the sentence starts. Because the library for the summary
#     just pulls the abstract, which is just a "snippet of text from the beginning of the article"
#

# Let's try not to break lists again. Let's be extra specially careful with that.
# Might need to use the page.html() for that one (cause content doesn't return lists)

# For sections that are too short, can't do much if there is no implict section
# When pulling from a section, any section, get 500 characters. Then, if the sentence has not ended, pull the rest. If < 500, just pull the whole thing
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
