import glob,csv,json, numpy as np,pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.datasets.dump_svmlight_file
from multiprocessing import Pool
from functools import reduce

def linewiseFeatures(a,b):
  """Adds line--b--to features: a """
  j = json.loads(b)
  return a + "\n\n" + j.get('body','')

def fileToFeatures(f):
  """Get features from filepath"""
  payload = f.split("/")[-1]
  sub,y,m,d,e = payload.split("-")
  text = reduce(linewiseFeatures,open(f),{}) 
  return {"text":text,"sub":sub,"year":y,
          "month":m,"day":d,"end":e[:-4]}

if __name__ == "__main__":
   fs = glob.glob("/scratch/jwolohan/CryptoPredicto/data/*.txt")
   with Pool(processes=24) as p:
     fs = list(p.map(fileToFeatures,fs))
   CV = CountVectorizer(max_df=.95, min_df=.01)
   # Get feature matrix
   X = CV.fit_transform([f['text'] for f in fs])
   # Write feature matrix to file
   dump_svmlight_file(X=X,f="myBOW.sparse.matrix.svm")
   # Dump Vocab to file (for the future!)
   json.dump(CV.vocabulary_,"MyVocab.json")
   # Write the file descriptions to a file
   import pandas as pd
   df = pd.DataFrame(fs)
   df.drop('text').to_csv("./myFileData.csv")
