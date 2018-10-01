#author: Faith Kilonzi
#NLP Project Lab 2
#Minimum Edit Distance 

import sys

#function minEditDistance() to implement minimum edit distance algorithm
#@source parameter - string from which transformation happens
#@target parameter - string to which the source is changed to
def minEditDistance(source,target):
    insertionCost=1
    deletionCost=1
    substitutionCost=2
    n=len(source)

    m=len(target)

    D =[[0]*(m+1) for _ in range(n+1)]#the matrix D
    #initialization of base case values
    for i in range(0,n+1): 

        D[i][0]=i
    for j in range(0,m+1):

        D[0][j]=j
    #recurrence function to implement Edit Distance dynamically
    for i in range (1,n+1): #rows

        for j in range(1,m+1): #columns
            #when row value (top) is equal to column value (left)
            if source[i-1]==target[j-1]: 
                D[i][j] = D[i-1][j-1] 

            else :
                D[i][j] = min(D[i][j-1]+ insertionCost,   
                                   D[i-1][j]+ deletionCost,    
                                   D[i-1][j-1]+ substitutionCost) 

   
    print("Minimum edit distance between " + source +" and " +
          target +" is "+ str(D[i][j]))


#driver function to run the program to take user input
if __name__== "__main__":

    #error handling
    if len(sys.argv) == 3:
        minEditDistance(sys.argv[1], sys.argv[2])
    else:
        print ('You failed to provide enough parameters (2) !')
        sys.exit(1) 

    

    
