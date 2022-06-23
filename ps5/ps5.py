# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

from dataclasses import replace
from locale import normalize
from optparse import TitledHelpFormatter
from types import NoneType
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime, tzinfo, timedelta, timezone
from pytz import timezone
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

class PhraseTrigger(Trigger):

    def is_phrase_in(self):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError

class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text, phrase):
        clean_title = "".join([(n.lower() if n not in string.punctuation else " ") for n in text])
        use_title_list = clean_title.split()
        clean_phrase = "".join([(n.lower() if n not in string.punctuation else " ") for n in phrase])
        use_phrase_list = clean_phrase.split()
        for i in range(len(use_title_list)-(len(use_phrase_list)-1)):
            if use_phrase_list[0] == use_title_list[i]:
                for m in range(len(use_phrase_list)):
                    if use_phrase_list[m] == use_title_list[m+i]:
                        if m == len(use_phrase_list)-1:
                            return True
    
    def evaluate(self, story):
        if self.is_phrase_in(story.get_title(), self.phrase) == True:
            return True


# Problem 4
#DescriptionTrigger

class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text, phrase):
        clean_title = "".join([(n.lower() if n not in string.punctuation else " ") for n in text])
        use_title_list = clean_title.split()
        clean_phrase = "".join([(n.lower() if n not in string.punctuation else " ") for n in phrase])
        use_phrase_list = clean_phrase.split()
        for i in range(len(use_title_list)-(len(use_phrase_list)-1)):
            if use_phrase_list[0] == use_title_list[i]:
                for m in range(len(use_phrase_list)):
                    if use_phrase_list[m] == use_title_list[m+i]:
                        if m == len(use_phrase_list)-1:
                            return True

    def evaluate(self, story):
        if self.is_phrase_in(story.get_description(), self.phrase) == True:
            return True

# TIME TRIGGERS

# Problem 5

class TimeTrigger(Trigger):
    def time_check(self):
        raise NotImplementedError

    def evaluate(self):
        raise NotImplementedError
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6
# TODO: BeforeTrigger and AfterTrigger

class BeforeTrigger(TimeTrigger):
    def __init__(self, moment):
        tz_moment = moment
        self.moment = datetime.strptime(tz_moment, '%d %b %Y %H:%M:%S')
            
    def time_check(self, pubdate):
        try:
            if pubdate < self.moment:
                return True
        except:
            #self.moment = self.moment.astimezone(pytz.timezone("EST"))
            self.moment = self.moment.replace(tzinfo=pytz.timezone('EST'))
            if pubdate < self.moment:
                return True

    def evaluate(self, story):
        if self.time_check(story.get_pubdate()):
            return True

class AfterTrigger(TimeTrigger):
    def __init__(self, moment):
        tz_moment =  moment
        self.moment = datetime.strptime(tz_moment, '%d %b %Y %H:%M:%S')

    def time_check(self, pubdate):
        try:
            if pubdate > self.moment:
                return True
        except:
            #self.moment = self.moment.astimezone(pytz.timezone("EST"))
            self.moment =self.moment.replace(tzinfo=pytz.timezone('EST'))
            if pubdate > self.moment:
                return True

    def evaluate(self, story):
        if self.time_check(story.get_pubdate()) == True:
            return True


# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    def evaluate(self, story):
        if self.trigger.evaluate(story) != True:
            return True


# Problem 8
# TODO: AndTrigger

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        if self.trigger1.evaluate(story) and self.trigger2.evaluate(story) == True:
            return True

# Problem 9
# TODO: OrTrigger

class OrTrigger(AndTrigger):

    def evaluate(self, story):
        if self.trigger1.evaluate(story) or self.trigger2.evaluate(story) == True:
            return True


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    triggered_stories = []

    for i in range(len(stories)):
        for j in triggerlist:
            if j.evaluate(stories[i]) == True:
                triggered_stories.append(stories[i])
                

    #triggered_stories = [(s if (j.evaluate(s) is True for j in triggerlist) == True else None) for s in stories]
    #print (triggered_stories)
    return triggered_stories

    



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    trigger_list = []
    comp_dict = {}

    for i in range(len(lines)):
        line = lines[i].split(',')
        if line[1] == 'TITLE':
            comp_dict[line[0]] = TitleTrigger(line[2])
        if line[1] == 'DESCRIPTION':
            comp_dict[line[0]] = DescriptionTrigger(line[2])
        if line[1] == 'BEFORE':
            comp_dict[line[0]] = BeforeTrigger(line[2])
        if line[1] == 'AFTER':
            comp_dict[line[0]] = AfterTrigger(line[2])
        if line[1] == 'AND':
            comp_dict[line[0]] = AndTrigger(line[2], line[3])
        if line[0] == 'ADD':
            for j in range(1, len(line)):
                trigger_list.append(comp_dict.get(line[j]))
        
    return trigger_list



    print(lines) # for now, print it so you see what it contains!

read_trigger_config('triggers.txt')



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        # triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

