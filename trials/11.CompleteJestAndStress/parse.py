import csv

file2 = open("Jest_Final_Subjects.txt", "a")

with open('Jest_Subjects.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            file2.write(row[0])
            file2.write("\n")
            file2.write(row[1])
            file2.write("\n")
            line_count += 1

file2.close()
