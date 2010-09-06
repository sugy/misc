#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#import sys, pprint, time
import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)

import feedparser
from django.utils import feedgenerator

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


class MainHandler(webapp.RequestHandler):
    def get(self):

      try:
        query = self.request.query_string

        #feed_url = 'http://api.atnd.org/events/?format=atom&keyword=' + query
        feed_url = 'http://api.atnd.org/events/?format=atom&' + query
        feed = feedparser.parse( feed_url )
        if feed.bozo:
          raise Exception, 'Failed to fetch feed: %s' % feed_url
    
        #pp.pprint( feed )
    
        fncfeed=feedgenerator.Atom1Feed
        new_feed=fncfeed(
            title       = feed.feed.title +'::'+ query
          , link        = feed.feed.link
          , description = feed.feed.title +'::'+ query
          , language    = feed.feed.language
          )
    
        for entry in feed.entries:
          new_id = entry.id.rsplit(':',1)[0] +':/'+ entry.link.split('/',3)[3]
          
          #dt = entry.published_parsed
          dt = entry.updated_parsed
          pubdate = datetime.datetime( dt[0],dt[1],dt[2],dt[3],dt[4],dt[5],0,JST() )
          #pubdate = datetime.datetime( dt[0],dt[1],dt[2],dt[3],dt[4],dt[5] )
          #pubdate += datetime.timedelta(hours=9)
    
          new_feed.add_item(
              title       = entry.title
            , link        = entry.link
            , description = entry.subtitle
            , unique_id   = new_id
            , author_name = entry.author
            , pubdate     = pubdate
            )
    
        #pp.pprint( new_feed.writeString( feed.encoding ) )
        self.response.headers['Content-Type']=feed.headers['content-type']
        self.response.out.write(new_feed.writeString( feed.encoding ))
    
      except Exception, e:
        self.response.out.write(e)
        #pp.pprint(e)
        #pass


class JST(datetime.tzinfo):
    def utcoffset(self,dt):
        return datetime.timedelta(hours=9)
    def dst(self,dt):
        return datetime.timedelta(0)
    def tzname(self,dt):
        return "JST"


def main():
    application = webapp.WSGIApplication([('/.*', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
