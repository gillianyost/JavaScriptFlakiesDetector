file1 = open('top100.txt', 'r')
Lines = file1.readlines()
  
for line in Lines:
    splitVar = (line.split())
    packageName = splitVar[0].split("/")
    file2 = open("finaloutput.txt", "a")
    file2.write(packageName[1])
    file2.write("\n")
    file2.write(splitVar[-1])
    file2.write("\n")
    file2.close()

file1.close()