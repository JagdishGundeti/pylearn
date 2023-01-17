# Open a file
f = open("demofile2.txt", "a")
f.write("Now the file has more content!")
# Close opend file
f.close()


# Open a file
fo = open("demofile2.txt", "rb")
print(fo.read(10))
# Close opend file
fo.close()

# Open a file
fo1 = open("foo.txt", "w")
fo1.write( "Python is a great language.\nYeah its great!!\n")

# Close opend file
fo1.close()