#author: Faith Kilonzi
#NLP Project Lab 2
#Minimum Edit Distance 

import sys

#function to implement minimum edit distance algorithm
#@source parameter - string from which transformation happens
def minEditDistance(source,target):
    n=len(source)

    m=len(target)

    D =[[0]*(m+1) for _ in range(n+1)]#the matriD whose last element ->edit distance

    for i in range(0,n+1): #initialization of base case values

        D[i][0]=i
    for j in range(0,m+1):

        D[0][j]=j
    #recurrence function to implement dynamic Edit Distance
    for i in range (1,n+1):

        for j in range(1,m+1):

            if source[i-1]==target[j-1]:
                D[i][j] = D[i-1][j-1] 

            else :
                D[i][j]= min(D[i][j-1],D[i-1][j],D[i-1][j-1])+1

   
    print("Minimum edit distance between " + source +" and " +
          target +" is "+ str(D[i][j]))


#driver function to run the program
if __name__== "__main__":
    minEditDistance(sys.argv[1], sys.argv[2])

    
