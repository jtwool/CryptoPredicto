import glob,json
from functools import reduce
from multiprocessing import Pool
from sklearn.feature_extraction.text import CountVectorizer

def file2Text(f):
  with open(f) as openF:
    return [json.loads(l).get('body','') for l in openF]

if __name__ == "__main__":
  with Pool(processes=20) as p:
    texts = p.map(file2Text,glob.iglob("./data/*.txt"))
  texts = reduce(lambda a,b:a+b, texts)
  CV = CountVectorizer(max_df=.95,min_df=.005)
  CV.fit(texts)
  with open("vocabulary.txt",'w') as w:
    for k in sorted(CV.vocabulary_.keys()):
      w.write(f"{k}\n")
    

