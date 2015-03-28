#! /usr/bin/env python3

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
    while True:
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
