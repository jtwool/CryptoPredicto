import glob,csv,json
from functools import reduce

def getSentiment(s):
  """Get the sentiment score of a string"""
  pass

def linewiseFeatures(a,b):
  """Adds line--b--to features: a """
  j = json.loads(b)
  txt = j['body']
  a['textAll'] = a.get('textAll'," ") + " " + txt
  a['posts'] = a.get('posts',0) + 1
  a['uusers'] = a.get('uusers',set()) | j['author']
  a['score'] = a.get('score',[]) + list(j['score'])
  a['wordcount'] = a.get('wordcount',[]) + list(len(txt.split()))
  a['sentiment'] = a.get('sentiment',[]) + list(getSentiment(txt))
  return a

def daywiseFeatures(d):
  """Calculates summary features for day, returns matrix"""
  d['scoreAvg'] = 0
  d['scoreMax'] = 0
  d['numUsers'] = len(d['uusers'])
  d['sentAverage'] = 0 
  d['sentPositive'] = 0
  d['sentNegative'] = 0
  d['sentHi'] = 0
  d['sentLo'] = 0
  d['sentNet'] = 0
  d['sentPosSum'] = 0
  d['sentNegSum'] = 0
  return d

def fileToFeatures(f):
  """turn files into feature matricies"""
  accumulated = reduce(linewiseFeatures,open(f),{}) 
  m = daywiseFeatures(accumulated)
  return m

if __name__ == "__main__":
   fs = glob.glob("/scratch/jwolohan/CryptoPredicto/*.txt")
   fs = map(fileToFeatures,fs)
   with open("/scratch/jwolohan/CrpytoPredicto/Features.csv",'w') as f:
     csv.DictWriter(f,fieldnames=[])
