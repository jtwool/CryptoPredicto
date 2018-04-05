import glob,csv,json, numpy as np
from multiprocessing import Pool
from functools import reduce

class SentiAnalyzer:
  def __init__(self):
    self.lex = {}

  def loadLexicon(self,fp):
    for line in open(fp):
      tkn,score,_,_ = line.split()
      self.lex[tkn]=float(score)

  def lookupWord(self,word):
    return self.lex.get(word,0.0)

  def analyzeText(self,text):
    txt = text.lower().split()
    scores = map(self.lookupWord,txt)
    return sum(scores)

NRC = SentiAnalyzer()
NRC.loadLexicon("NRC-unigrams.txt")

def linewiseFeatures(a,b):
  """Adds line--b--to features: a """
  j = json.loads(b)
  txt = j['body']
  a['textAll'] = a.get('textAll',' ') + " " + txt
  a['posts'] = a.get('posts',0) + 1
  a['uusers'] = a.get('uusers',set()) | set([j['author']])
  a['score'] = a.get('score',[]) + [j['score']]
  a['wordcount'] = a.get('wordcount',[]) + [len(txt.split())]
  a['sentiment'] = a.get('sentiment',[]) + [NRC.analyzeText(txt)]
  return a

def daywiseFeatures(d):
  """Calculates summary features for day, returns matrix"""
  d['score'] = d.get('score',[0])
  d['sentiment'] = d.get('sentiment',[0])
  d['wordcount'] = d.get('wordcount',[0])
  d['uusers'] = d.get('uusers',[])
  d['textAll'] = d.get('textAll',"")
  d['scoreAvg'] = np.mean(d.get('score'))
  d['scoreMax'] = np.max(d.get('score'))
  d['numUsers'] = len(d.get('uusers'))
  d['sentAverage'] = np.mean(d.get('sentiment'))
  d['sentPositive'] = len(list(filter(lambda x:x>0,d['sentiment'])))
  d['sentNegative'] = len(list(filter(lambda x:x<0,d['sentiment'])))
  d['sentHi'] = np.max(d['sentiment'])
  d['sentLo'] = np.min(d['sentiment'])
  d['sentSum'] = sum(d['sentiment'])
  d['sentPosSum'] = sum(filter(lambda x:x>0, d['sentiment']))
  d['sentNegSum'] = sum(filter(lambda x:x<0, d['sentiment']))
  d['wordsAvg'] = np.mean(d['wordcount'])
  d['wordsTot'] = np.sum(d['wordcount'])
  d.pop('textAll'); d.pop('wordcount'); d.pop('sentiment'); d.pop('uusers'); d.pop('score')
  return d

def fileToFeatures(f):
  """turn files into feature matricies"""
  accumulated = reduce(linewiseFeatures,open(f),{}) 
  m = daywiseFeatures(accumulated)
  return m

if __name__ == "__main__":
   fs = glob.glob("/scratch/jwolohan/CryptoPredicto/data/*.txt")
   with Pool(processes=24) as p:
     fs = list(p.map(fileToFeatures,fs))
   import pandas as pd
   pd.DataFrame(fs).to_csv("./myFeatures.csv")
