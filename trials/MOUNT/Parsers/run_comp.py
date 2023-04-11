import sys
import csv
import os
import json


if __name__ == '__main__':
    file1_flakies = []
    file2_flakies = []
    file1_flakies_dict = {}
    file2_flakies_dict = {}

    with open(sys.argv[1], newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for row in data:
                tmp = {}
                head, tail = os.path.split(row[0])
                value = tail + row[1]
                file1_flakies.append(value)
                tmp['failures'] = row[2]
                tmp['reason'] = row[3]
                file1_flakies_dict[value] = tmp

    with open(sys.argv[2], newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',')
            for row in data:
                tmp = {}
                head, tail = os.path.split(row[0])
                value = tail + row[1]
                file2_flakies.append(value)
                tmp['failures'] = row[2]
                tmp['reason'] = row[3]
                file2_flakies_dict[value] = tmp

    # with open(sys.argv[3]) as file:
    #     data = json.load(file)

    common_list = set(file1_flakies).intersection(file2_flakies)
    onlyFile1 = list(set(file1_flakies) - set(file2_flakies))
    onlyFile2 = list(set(file2_flakies) - set(file1_flakies))
    commonNum = len(common_list)
    onlyFile1Num = len(onlyFile1)
    onlyFile2Num = len(onlyFile2)

    f = open(sys.argv[3], 'w')
    # print(common_list)
    f.write(str(commonNum))
    f.write('\n\n')
    for item in common_list:
        f.write(item)
        f.write("\n" + sys.argv[1] + " Failures: " + file1_flakies_dict[item]['failures'] + "   Reason: " + file1_flakies_dict[item]['reason'])
        f.write("\n" + sys.argv[2] + " Failures: " + file2_flakies_dict[item]['failures'] + "   Reason: " + file1_flakies_dict[item]['reason'])
        f.write("\n\n")

    f.close()
    
    f = open(sys.argv[4], 'w')
    # print(common_list)
    f.write(str(onlyFile1Num))
    f.write('\n\n')
    for item in onlyFile1:
        f.write(item)
        f.write("\n" + sys.argv[1] + " Failures: " + file1_flakies_dict[item]['failures'] + "\n")
        f.write(sys.argv[1] + " Reason: " + file1_flakies_dict[item]['reason'] + "\n")
        f.write("\n\n")
    f.close()

    f = open(sys.argv[5], 'w')
    # print(common_list)
    f.write(str(onlyFile2Num))
    f.write('\n\n')
    for item in onlyFile2:
        f.write(item)
        f.write("\n" + sys.argv[2] + " Failures: " + file2_flakies_dict[item]['failures'] + "\n")
        f.write(sys.argv[2] + " Reason: " + file2_flakies_dict[item]['reason'] + "\n")
        f.write("\n\n")
    f.close()
    print("Comparison of flakie tests in " + sys.argv[1] + " and " + sys.argv[2] + " Completed.\n")
