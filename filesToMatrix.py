import glob,csv
from functools import reduce

def linewiseFeatures(a,b):
  """Adds line--b--to features: a """
  pass

def daywiseFeatures(d):
  """Collects summary features for day"""
  pass

def fileToFeatures(f):
  """I turn files into feature matricies"""
  accumulated = reduce(linewiseFeatures,open(f),[]) 
  m = daywiseFeatures(accumulated)
  return m

if __name__ == "__main__":
   fs = glob.glob("/scratch/jwolohan/CryptoPredicto/*.txt")
   fs = map(fileToFeatures,fs)
   with open("/scratch/jwolohan/CrpytoPredicto/Features.csv",'w') as f:
     csv.DictWriter(f,fieldnames=[])
   
     

