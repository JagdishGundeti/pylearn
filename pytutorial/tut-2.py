

# for i in range(5):
#   print(i)

# for i in range(0,5):
#     print(i)

for i in range(0,5,2):
    print(i)


ls = ['as', 33, 34.3, "adsfasd"]
ls.append("ooo")
print(ls)

dict = {}
dict['one'] = "This is one"
dict[2]     = "This is two"

tinydict = {'name': 'john','code':6734, 'dept': 'sales'}

print (dict.keys())
print (dict.values())

print (dict['one'])       # Prints value for 'one' key
print (dict[2])           # Prints value for 2 key
print (tinydict)          # Prints complete dictionary
print (tinydict.keys())   # Prints all the keys
print (tinydict.values()) # Prints all the values


a = True
# display the value of a
print(a)

# display the data type of a
print(type(a))