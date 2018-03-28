import glob,csv

def fileToFeatures(f):
  

if __name__ == "__main__":
   fs = glob.glob("/scratch/jwolohan/CryptoPredicto/*.txt")
   fs = map(fileToFeatures,fs)
   with open("/scratch/jwolohan/CrpytoPredicto/Features.csv",'w') as f:
     csv.DictWriter(f,fieldnames=[])
   
     

