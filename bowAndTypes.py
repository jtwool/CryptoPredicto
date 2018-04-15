import glob,csv,json, numpy as np,pickle
from sklearn.feature_extraction.text import CountVectorizer
from scipy.io import mmwrite 
from multiprocessing import Pool
from functools import reduce
import toolz
import pandas as pd

def linewiseFeatures(a,b):
  """Adds line--b--to features: a """
  j = json.loads(b)
  return a + "\n\n" + j.get('body','')

def fileToFeatures(f):
  """Get features from filepath"""
  payload = f.split("/")[-1]
  sub,y,m,d,e = payload.split("-")
  text = reduce(linewiseFeatures,open(f),"") 
  return {"sub":sub,"year":y,
          "month":m,"day":d,"end":e[:-4],"text":text}

if __name__ == "__main__":
   fs = glob.glob("/scratch/jwolohan/CryptoPredicto/data/*.txt")
   with Pool(processes=24) as p:
     fs = list(p.map(fileToFeatures,fs))
   gs = toolz.groupby(lambda x:x.get('sub')+x.get('end'),fs)
   for k,fs in gs.items():
     CV = CountVectorizer(max_df=.95, min_df=.01)
     X = CV.fit_transform([f['text'] for f in fs])
     mmwrite(a=X,target=f"myBOW.sparse.matrix.{k}.mtx")
     json.dump(list(CV.vocabulary_.keys()),open(f"MyVocab.{k}.json",'w'))
     df = pd.DataFrame(fs) 
     df.to_csv(f"./myBOWfeatures.{k}.csv")
