#!/usr/bin/python

# Function definition is here
def printinfo( arg1, *vartuple ):
   "This prints a variable passed arguments"
   print("Output is: ")
   for var in vartuple:
        print(var)
   return;

# Now you can call printinfo function
printinfo( 10 )
printinfo( 70, 60, 50 )

# Function definition is here
sum = lambda arg1, arg2: arg1 * arg2;

# Now you can call sum as a function
printinfo( "Value of total : ", sum( 10, 20 ) )
printinfo( "Value of total : ", sum( 20, 20 ) )