

from math import *
def importfiles(filename):
	file=open(filename,"r").readlines()
	ndoc=len(file)
	Ccount={}
	Cwords={}
	Cbackets={}

	V={}
	for i in file:
		breaklin=i.split('\t')
		if breaklin[1].strip("\n") in Ccount.keys():
			Ccount[breaklin[1].strip("\n")]+=1
			Cbackets[breaklin[1].strip("\n")] += breaklin[0].strip(".").strip("\t1\n").split(" ")
			for k in breaklin[0].strip(".").strip("\t1\n").split(" "):
				V[k] = 0
				if k in Cwords[breaklin[1].strip("\n")].keys():
					Cwords[breaklin[1].strip("\n")][k] += 1
				else:
					Cwords[breaklin[1].strip("\n")][k] = 1
			
		else:
			Ccount[breaklin[1].strip("\n")] =1
			Cbackets[breaklin[1].strip("\n")] = breaklin[0].strip(".").strip("\t1\n").split(" ")
			Cwords[breaklin[1].strip("\n")] = {}
			for k in breaklin[0].strip(".").strip("\t1\n").split(" "):
				V[k] = 0
				if k in Cwords[breaklin[1].strip("\n")].keys():
					Cwords[breaklin[1].strip("\n")][k] += 1
				else:
					Cwords[breaklin[1].strip("\n")][k] = 1

	return V,ndoc,Cwords,Ccount, Cbackets


def computeDenominator(bigdoc,V):
	count=0
	for w in V:
		count+=bigdoc.count(w)

	return count+len(V)



def train_NaiveBayes(C,ndoc,Ccount,Cwords,V,Cbackets):
	logpriors={}
	loglikelihoods={}
	for c in C:
		loglikelihoods[c]={}
		nc=Ccount[c]
		logpriorc=log(nc/ndoc)
		bigdoc=Cbackets[c]
		den=computeDenominator(bigdoc,Cbackets)
		for w in V:
			countwc=bigdoc.count(w)
			loglikelihoodwc=log((countwc+1)/den)
			loglikelihoods[c][w]=loglikelihoodwc
		logpriors[c]=logpriorc
		

	return logpriors,loglikelihoods



def testNaiveBayes(testdoc,logprior,loglikelihood,C,V):
	sumcs = {}
	argmax=-100000000
	lclass=None

	for c in C:
		sumc = logprior[c]
		for i in testdoc.split(" "):
			w=i
			if w in V:
				sumc = sumc + loglikelihood[c][w]
		sumcs[c]=sumc

		if sumc>argmax:
			lclass=c
			argmax = sumc

	return lclass




def main(filename):
	V,ndoc,Cwords,Ccount, Cbackets = importfiles(filename)
	logpriors,loglikelihoods = train_NaiveBayes(Ccount.keys(),ndoc,Ccount,Cwords,V,Cbackets)
	test = open("test.txt").readlines()
	count = 0
	res=" "
	resultsfile= open("results_file.txt", "w")
	for i in test:
		splited = i.split("\t")
		#print(testNaiveBayes(splited[0],logpriors,loglikelihoods,Cwords.keys(),V), splited[1].strip("\n"))
		res=testNaiveBayes(splited[0],logpriors,loglikelihoods,Cwords.keys(),V), splited[1].strip("\n") +'\n'
		res =' '.join(res)
		if testNaiveBayes(splited[0],logpriors,loglikelihoods,Cwords.keys(),V) == splited[1].strip("\n"):
			count += 1
		resultsfile.write(res)
	#print(count, "/", len(test))
		

main('training.txt')
	
	



