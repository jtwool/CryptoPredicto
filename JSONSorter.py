import json, glob, toolz
import datetime as dt
from toolz.itertoolz import groupby

def toBetterThing(line):
  j = json.loads(line)
  d = dt.datetime.fromtimestamp(j['created_utc'])
  j['dayCreated'] = d.strftime("%Y-%m-%d")
  j['timeCreated'] = int(d.strftime("%H"))
  return j

if __name__ == "__main__":
  months = glob.glob("./*-Coins.txt")
  for month in months:
    subreddits = groupby(lambda x:json.loads(x).get('subreddit'),open(month,'r'))
    for subreddit in subreddits.keys():
      monthlyPosts = map(toBetterThing, subreddits[subreddit])
      byDay = groupby(lambda x:x.get('dayCreated'), monthlyPosts)
      for day in byDay.keys():
        allDay = open(f"{subreddit}-{day}-allDay.txt",'w')
        shortDay = open(f"{subreddit}-{day}-3pm.txt",'w')
        for post in byDay[day]:
          allDay.write(json.dumps(post)+"\n")
          if post.get('timeCreated') <= 15:
            shortDay.write(json.dumps(post)+"\n") 
