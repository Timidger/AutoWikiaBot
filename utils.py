#!/usr/bin/python3
"""General collection of utilites, mostly operating on Reddit"""

import re
import urllib
from wikia import wikia

def find_link(body):
    begin_index = body.find("http://")
    for index, char in enumerate(body[begin_index:]):
        if char in (" ", ")", "\n"):
            end_index = index + begin_index
            break
    else:
        end_index = None # This goes right to the end of the string
    link = body[begin_index: end_index]
    return link

def find_sub_wikia(link):
    # Just after http://, maybe should be more explicit here
    start_index = link.find("//") + 2
    end_index = link.find(".")
    if wikia.LANG:
        start_index = end_index
        end_index = link.find(".", start_index + 1)
    return link[start_index:end_index]

def find_article(link):
    begin_index = link.rfind("/") + 1
    article_name = link[begin_index:]
    article_name = urllib.parse.unquote(article_name)
    return article_name

def summarize(page) -> str:
    """Retrieves a complete summary of a WikiaPage, i.e one that doesn't cut
    off in the middle of a sentence."""
    summary = page.summary
    # It stops abruptly in the middle of the summary
    if summary.endswith("..."):
       # Remove the last three characters, which we just showed are "..."
       summary = summary[:-3]

      # page.summary removes all newlines from content, so we have to do that
       content = page.content.replace("\n", " ")
       assert content.find(summary) != -1, "Summary is not in content!"

       # Partition so that the third partition is the rest of the summary
       rest = content.partition(summary)[2]
       index = rest.find(".") + 1
       assert index != 0, "Couldn't find a period to end the the summary!"

       rest = rest[:index]
       summary += rest
    return summary

if __name__ == "__main__":
    # These are taken from the top 3 posts /u/autowikiabot has responded to
    luanne = "It's [Luanne](http://theoffice.wikia.com/wiki/Luanne). :)"
    ron = """what's even better, is that Ron Perlman is actually standing \
            behind the projector screen in the endgame room, \
            narrating the slides.

    http://fallout.wikia.com/wiki/Ron_the_Narrator

    (Yep, the Gamebryo engine actually requires an entity in game, \
            to deliver speech media.)"""
    burn_heal = "http://pokemon.wikia.com/wiki/Burn_Heal"

    # Testing Luanne post
    link = find_link(luanne)
    assert link == "http://theoffice.wikia.com/wiki/Luanne"
    sub_wikia = find_sub_wikia(link)
    assert sub_wikia == "theoffice"
    article = find_article(link)
    assert article == "Luanne"

    # Testing Ron post
    link = find_link(ron)
    assert link == "http://fallout.wikia.com/wiki/Ron_the_Narrator"
    sub_wikia = find_sub_wikia(link)
    assert sub_wikia == "fallout"
    article = find_article(link)
    assert article == "Ron_the_Narrator"

    # Testing Burn Heal Post
    link = find_link(burn_heal)
    assert link == "http://pokemon.wikia.com/wiki/Burn_Heal"
    sub_wikia = find_sub_wikia(link)
    assert sub_wikia == "pokemon"
    article = find_article(link)
    assert article == "Burn_Heal"
