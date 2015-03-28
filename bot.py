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
import sys
import praw
import utils
from wikia import wikia

BOT = praw.Reddit("autowikiabot by /u/timidger at /r/autowikiabot")
BOT.login("autowikiabot", "I lke JSON")

# The sub reddit that the bot scans on, usually /r/all
SUB_REDDIT = str(sys.argv[1])
# The template for the main header of the post, which contains the tile & url
POST_HEADER = "\n".join(("#####&#009;", "######&#009;", "####&#009;",
                        "[**{title}**]({link}):\n", "---\n"))

# The basic footer of a post, which contain info about the bot
POST_FOOTER = ("\n\n---\n"
    "^(Parent commenter can) [^toggle ^NSFW](http://www.np.reddit.com/message/"
    "compose?to=autowikiabot&subject=AutoWikibot NSFW toggle&message=%2Btoggle-"
    "nsfw+cj4ck5b) ^or [^delete](http://www.np.reddit.com/message/compos"
    "e?to=autowikiabot&subject=AutoWikibot Deletion&message=%2Bdelete+cj4ck5b)"
    "^(. Will also delete on comment score of -1 or less. |) [^(FAQs)]"
    "(http://www.np.reddit.com/r/autowikiabot/wiki/index) ^|  [^Source](https:/"
    "/github.com/Timidger/autowikiabot-py)")

def make_reply(page):
    """Constructs a reply summary using the given page"""
    header = POST_HEADER.format(title=page.title, link=page.url)
    # Get the basic body
    body = utils.summarize(page)
    # Make the first occurence of the title bolded
    body = body.replace(page.title, "__" + page.title + "__", 1)
    # Add the quote tags around everything (including each paragraph)
    body = ">\n" + body.replace("\n", "\n>")
    return header + body + POST_FOOTER



if __name__ == "__main__":
    try:
        for post in praw.helpers.comment_stream(BOT, SUB_REDDIT, verbosity=0):
            # Search for a wikia link in the post
            link = utils.find_link(post.body)
            if not link or "wikia.com" not in link:
                continue
            # Get the sub-wikia and article name
            sub_wikia = utils.find_sub_wikia(link)
            article = utils.find_article(link)

            # Construct the page using that data
            page = wikia.page(sub_wikia, article)
            # Get the summary of the page to post
            reply = make_reply(page)
            print("Replied with {} from {}".format(page.title, page.sub_wikia).encode("ascii", "ignore"))
            post.reply(reply)
    except Exception as e:
        print("ERROR: ", e)
